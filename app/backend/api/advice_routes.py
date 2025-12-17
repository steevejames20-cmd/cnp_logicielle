import io
import csv
from datetime import date, datetime
from collections import defaultdict
from statistics import mean

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fpdf import FPDF
from sqlalchemy.orm import Session

from app.backend.core.security import get_current_user_optional
from app.backend.core.database import get_db
from app.backend.models.budget import Budget
from app.backend.models.expense import Expense
from app.backend.models.saving_goal import SavingGoal
from app.backend.schemas.advice_schema import AdviceRead
from app.backend.models.user import User

router = APIRouter(tags=["advice", "stats", "export"])


def _budget_usage_advice(budget: Budget, expenses: list[Expense]) -> list[dict]:
    advices = []
    total_spent = sum(e.amount for e in expenses if e.budget_id == budget.id)
    usage = (total_spent / budget.amount) * 100 if budget.amount else 0
    if usage >= 80:
        advices.append(
            {
                "advice_text": f"Votre budget '{budget.name}' est consommé à {usage:.1f}% : pensez à ralentir.",
                "severity": "warning",
                "related_budget_id": budget.id,
            }
        )
    return advices


def _category_spend_advice(expenses: list[Expense]) -> list[dict]:
    advices = []
    by_category: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount
    if not by_category:
        return advices
    max_cat = max(by_category, key=by_category.get)
    advices.append(
        {
            "advice_text": f"La catégorie '{max_cat}' est la plus coûteuse ({by_category[max_cat]:.2f}). Surveillez-la.",
            "severity": "info",
            "related_category": max_cat,
        }
    )
    return advices


def _daily_average_advice(budget: Budget, expenses: list[Expense]) -> list[dict]:
    advices = []
    today = date.today()
    start_period = date(today.year, today.month, 1)
    period_days = (today - start_period).days + 1
    spent = sum(e.amount for e in expenses if e.budget_id == budget.id and e.date >= start_period)
    daily_avg = spent / period_days if period_days else spent
    period_divisor = {"daily": 1, "weekly": 7, "monthly": 30}.get(budget.period, 30)
    budget_daily = budget.amount / period_divisor
    if daily_avg > budget_daily:
        advices.append(
            {
                "advice_text": f"Dépense moyenne quotidienne {daily_avg:.2f}€ > budget/jour {budget_daily:.2f}€ pour '{budget.name}'.",
                "severity": "warning",
                "related_budget_id": budget.id,
            }
        )
    return advices


def _saving_delay_advice(goals: list[SavingGoal]) -> list[dict]:
    advices = []
    today = date.today()
    for g in goals:
        if g.deadline and g.deadline < today and g.saved_amount < g.target_amount:
            advices.append(
                {
                    "advice_text": f"Objectif '{g.name}' en retard : {g.saved_amount:.2f}/{g.target_amount:.2f}.",
                    "severity": "warning",
                }
            )
    return advices


def _advanced_patterns(expenses: list[Expense]) -> list[dict]:
    advices = []
    by_week: dict[int, list[float]] = defaultdict(list)
    for e in expenses:
        iso = e.date.isocalendar()
        by_week[iso[1]].append(e.amount)
    for week, amounts in by_week.items():
        if len(amounts) >= 3 and mean(amounts) > 0:
            advices.append(
                {
                    "advice_text": f"Semaine {week}: dépenses moyennes {mean(amounts):.2f}€. Essayez de réduire de 10% la semaine suivante.",
                    "severity": "info",
                }
            )
    return advices


def _personalized_saving(goals: list[SavingGoal]) -> list[dict]:
    advices = []
    for g in goals:
        remaining = g.target_amount - g.saved_amount
        if remaining <= 0:
            continue
        days_left = (g.deadline - date.today()).days if g.deadline else 90
        per_day = remaining / days_left if days_left > 0 else remaining
        advices.append(
            {
                "advice_text": f"Pour '{g.name}', épargnez environ {per_day:.2f}€/jour pour atteindre {g.target_amount:.2f}.",
                "severity": "info",
            }
        )
    return advices


@router.get("/advice/basic", response_model=list[AdviceRead])
def basic_advice(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    budgets = db.query(Budget).all()
    expenses = db.query(Expense).all()
    goals = db.query(SavingGoal).all()
    advices = []
    for budget in budgets:
        advices.extend(_budget_usage_advice(budget, expenses))
        advices.extend(_daily_average_advice(budget, expenses))
    advices.extend(_category_spend_advice(expenses))
    advices.extend(_saving_delay_advice(goals))
    return [_to_advice_read(a) for a in advices]


def _to_advice_read(data: dict) -> AdviceRead:
    return AdviceRead(
        id=0,
        advice_text=data.get("advice_text", ""),
        severity=data.get("severity", "info"),
        related_budget_id=data.get("related_budget_id"),
        related_category=data.get("related_category"),
        created_at=datetime.utcnow(),
    )


@router.get("/advice/advanced", response_model=list[AdviceRead])
def advanced_advice(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    if not current_user or not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium required for advanced advice")
    expenses = db.query(Expense).all()
    goals = db.query(SavingGoal).all()
    advices = _advanced_patterns(expenses) + _personalized_saving(goals)
    return [_to_advice_read(a) for a in advices]


@router.get("/stats/summary")
def stats_summary(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    expenses = db.query(Expense).all()
    budgets = db.query(Budget).all()
    by_category: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount
    total_spent = sum(by_category.values())
    total_budget = sum(b.amount for b in budgets)
    return {
        "total_spent": total_spent,
        "total_budget": total_budget,
        "categories": by_category,
    }


@router.get("/stats/projection")
def stats_projection(db: Session = Depends(get_db)):
    today = date.today()
    start_period = date(today.year, today.month, 1)
    expenses = db.query(Expense).filter(Expense.date >= start_period).all()
    days_passed = (today - start_period).days + 1
    avg_daily = sum(e.amount for e in expenses) / days_passed if days_passed else 0
    days_in_month = 30
    projected = avg_daily * days_in_month
    return {"average_daily": avg_daily, "projected_month_end": projected}


def _export_rows(db: Session):
    budgets = db.query(Budget).all()
    expenses = db.query(Expense).all()
    rows = [("budget_id", "budget_name", "expense_id", "amount", "category", "date")]
    for e in expenses:
        budget = next((b for b in budgets if b.id == e.budget_id), None)
        rows.append((e.budget_id, budget.name if budget else "", e.id, e.amount, e.category, e.date.isoformat()))
    return rows


@router.post("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    rows = _export_rows(db)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=budgetis.csv"},
    )


@router.post("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    rows = _export_rows(db)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Budgetis Export", ln=True, align="C")
    for row in rows:
        pdf.cell(200, 10, txt=" | ".join(str(x) for x in row), ln=True)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=budgetis.pdf"},
    )

import io
import csv
from datetime import date, datetime
from collections import defaultdict
from statistics import mean

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from fpdf import FPDF
from sqlalchemy.orm import Session

from app.backend.core.security import get_current_user_optional
from app.backend.core.database import get_db
from app.backend.models.budget import Budget
from app.backend.models.expense import Expense
from app.backend.models.saving_goal import SavingGoal
from app.backend.schemas.advice_schema import AdviceRead
from app.backend.models.user import User

router = APIRouter(tags=["advice", "stats", "export"])


def _budget_usage_advice(budget: Budget, expenses: list[Expense]) -> list[dict]:
    advices = []
    total_spent = sum(e.amount for e in expenses if e.budget_id == budget.id)
    usage = (total_spent / budget.amount) * 100 if budget.amount else 0
    if usage >= 80:
        advices.append(
            {
                "advice_text": f"Votre budget '{budget.name}' est consommé à {usage:.1f}% : pensez à ralentir.",
                "severity": "warning",
                "related_budget_id": budget.id,
            }
        )
    return advices


def _category_spend_advice(expenses: list[Expense]) -> list[dict]:
    advices = []
    by_category: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount
    if not by_category:
        return advices
    max_cat = max(by_category, key=by_category.get)
    advices.append(
        {
            "advice_text": f"La catégorie '{max_cat}' est la plus coûteuse ({by_category[max_cat]:.2f}). Surveillez-la.",
            "severity": "info",
            "related_category": max_cat,
        }
    )
    return advices


def _daily_average_advice(budget: Budget, expenses: list[Expense]) -> list[dict]:
    advices = []
    today = date.today()
    start_period = date(today.year, today.month, 1)
    period_days = (today - start_period).days + 1
    spent = sum(e.amount for e in expenses if e.budget_id == budget.id and e.date >= start_period)
    daily_avg = spent / period_days if period_days else spent
    period_divisor = {"daily": 1, "weekly": 7, "monthly": 30}.get(budget.period, 30)
    budget_daily = budget.amount / period_divisor
    if daily_avg > budget_daily:
        advices.append(
            {
                "advice_text": f"Dépense moyenne quotidienne {daily_avg:.2f}€ > budget/jour {budget_daily:.2f}€ pour '{budget.name}'.",
                "severity": "warning",
                "related_budget_id": budget.id,
            }
        )
    return advices


def _saving_delay_advice(goals: list[SavingGoal]) -> list[dict]:
    advices = []
    today = date.today()
    for g in goals:
        if g.deadline and g.deadline < today and g.saved_amount < g.target_amount:
            advices.append(
                {
                    "advice_text": f"Objectif '{g.name}' en retard : {g.saved_amount:.2f}/{g.target_amount:.2f}.",
                    "severity": "warning",
                }
            )
    return advices


def _advanced_patterns(expenses: list[Expense]) -> list[dict]:
    advices = []
    by_week: dict[int, list[float]] = defaultdict(list)
    for e in expenses:
        iso = e.date.isocalendar()
        by_week[iso[1]].append(e.amount)
    for week, amounts in by_week.items():
        if len(amounts) >= 3 and mean(amounts) > 0:
            advices.append(
                {
                    "advice_text": f"Semaine {week}: dépenses moyennes {mean(amounts):.2f}€. Essayez de réduire de 10% la semaine suivante.",
                    "severity": "info",
                }
            )
    return advices


def _personalized_saving(goals: list[SavingGoal]) -> list[dict]:
    advices = []
    for g in goals:
        remaining = g.target_amount - g.saved_amount
        if remaining <= 0:
            continue
        days_left = (g.deadline - date.today()).days if g.deadline else 90
        per_day = remaining / days_left if days_left > 0 else remaining
        advices.append(
            {
                "advice_text": f"Pour '{g.name}', épargnez environ {per_day:.2f}€/jour pour atteindre {g.target_amount:.2f}.",
                "severity": "info",
            }
        )
    return advices


@router.get("/advice/basic", response_model=list[AdviceRead])
def basic_advice(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    budgets = db.query(Budget).all()
    expenses = db.query(Expense).all()
    goals = db.query(SavingGoal).all()
    advices = []
    for budget in budgets:
        advices.extend(_budget_usage_advice(budget, expenses))
        advices.extend(_daily_average_advice(budget, expenses))
    advices.extend(_category_spend_advice(expenses))
    advices.extend(_saving_delay_advice(goals))
    # Persist logs
    return [_to_advice_read(a) for a in advices]


def _to_advice_read(data: dict) -> AdviceRead:
    return AdviceRead(
        id=0,
        advice_text=data.get("advice_text", ""),
        severity=data.get("severity", "info"),
        related_budget_id=data.get("related_budget_id"),
        related_category=data.get("related_category"),
        created_at=datetime.utcnow(),
    )


@router.get("/advice/advanced", response_model=list[AdviceRead])
def advanced_advice(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    if not current_user or not current_user.is_premium:
        raise HTTPException(status_code=403, detail="Premium required for advanced advice")
    expenses = db.query(Expense).all()
    goals = db.query(SavingGoal).all()
    advices = _advanced_patterns(expenses) + _personalized_saving(goals)
    return [_to_advice_read(a) for a in advices]


@router.get("/stats/summary")
def stats_summary(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    expenses = db.query(Expense).all()
    budgets = db.query(Budget).all()
    by_category: dict[str, float] = defaultdict(float)
    for e in expenses:
        by_category[e.category] += e.amount
    total_spent = sum(by_category.values())
    total_budget = sum(b.amount for b in budgets)
    return {
        "total_spent": total_spent,
        "total_budget": total_budget,
        "categories": by_category,
    }


@router.get("/stats/projection")
def stats_projection(db: Session = Depends(get_db)):
    today = date.today()
    start_period = date(today.year, today.month, 1)
    expenses = db.query(Expense).filter(Expense.date >= start_period).all()
    days_passed = (today - start_period).days + 1
    avg_daily = sum(e.amount for e in expenses) / days_passed if days_passed else 0
    days_in_month = 30
    projected = avg_daily * days_in_month
    return {"average_daily": avg_daily, "projected_month_end": projected}


def _export_rows(db: Session):
    budgets = db.query(Budget).all()
    expenses = db.query(Expense).all()
    rows = [("budget_id", "budget_name", "expense_id", "amount", "category", "date")]
    for e in expenses:
        budget = next((b for b in budgets if b.id == e.budget_id), None)
        rows.append((e.budget_id, budget.name if budget else "", e.id, e.amount, e.category, e.date.isoformat()))
    return rows


@router.post("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    rows = _export_rows(db)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(rows)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=budgetis.csv"},
    )


@router.post("/export/pdf")
def export_pdf(db: Session = Depends(get_db)):
    rows = _export_rows(db)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Budgetis Export", ln=True, align="C")
    for row in rows:
        pdf.cell(200, 10, txt=" | ".join(str(x) for x in row), ln=True)
    pdf_bytes = pdf.output(dest="S").encode("latin-1")
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=budgetis.pdf"},
    )


