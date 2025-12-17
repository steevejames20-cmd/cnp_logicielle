from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.budget import Budget
from app.backend.models.expense import Expense
from app.backend.models.user import User
from app.backend.schemas.expense_schema import ExpenseCreate, ExpenseRead

router = APIRouter(prefix="/expense", tags=["expense"])


def _ensure_budget_access(budget: Budget, user: User | None):
    if budget.user_id is None:
        return
    if not user or user.id != budget.user_id:
        raise HTTPException(status_code=403, detail="Not authorized on this budget")


@router.post("", response_model=ExpenseRead)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == payload.budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    _ensure_budget_access(budget, current_user)
    expense = Expense(**payload.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    query = db.query(Expense).join(Budget, Expense.budget_id == Budget.id)
    if current_user:
        return query.filter(Budget.user_id == current_user.id).all()
    return query.filter(Budget.user_id.is_(None)).all()


@router.get("/by-budget/{budget_id}", response_model=list[ExpenseRead])
def list_expenses_by_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    _ensure_budget_access(budget, current_user)
    return db.query(Expense).filter(Expense.budget_id == budget_id).all()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.budget import Budget
from app.backend.models.expense import Expense
from app.backend.models.user import User
from app.backend.schemas.expense_schema import ExpenseCreate, ExpenseRead

router = APIRouter(prefix="/expense", tags=["expense"])


def _ensure_budget_access(budget: Budget, user: User | None):
    if budget.user_id is None:
        return
    if not user or user.id != budget.user_id:
        raise HTTPException(status_code=403, detail="Not authorized on this budget")


@router.post("", response_model=ExpenseRead)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == payload.budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    _ensure_budget_access(budget, current_user)
    expense = Expense(**payload.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    query = db.query(Expense).join(Budget, Expense.budget_id == Budget.id)
    if current_user:
        return query.filter(Budget.user_id == current_user.id).all()
    return query.filter(Budget.user_id.is_(None)).all()


@router.get("/by-budget/{budget_id}", response_model=list[ExpenseRead])
def list_expenses_by_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    _ensure_budget_access(budget, current_user)
    return db.query(Expense).filter(Expense.budget_id == budget_id).all()


