from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.budget import Budget
from app.backend.schemas.budget_schema import BudgetCreate, BudgetRead, BudgetUpdate
from app.backend.models.user import User

router = APIRouter(prefix="/budget", tags=["budget"])


def _ensure_budget_limit(db: Session, user: User | None):
    is_premium = bool(user and user.is_premium)
    if is_premium:
        return
    user_filter = Budget.user_id == user.id if user else Budget.user_id.is_(None)
    count = db.query(Budget).filter(user_filter).count()
    if count >= settings.free_budget_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Free tier limited to {settings.free_budget_limit} budgets. Upgrade for more.",
        )


@router.post("", response_model=BudgetRead)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    _ensure_budget_limit(db, current_user)
    budget = Budget(
        name=payload.name,
        amount=payload.amount,
        period=payload.period,
        user_id=current_user.id if current_user else None,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("", response_model=list[BudgetRead])
def list_budgets(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    if current_user:
        return db.query(Budget).filter(Budget.user_id == current_user.id).all()
    return db.query(Budget).filter(Budget.user_id.is_(None)).all()


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    return budget


@router.put("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: int,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(budget)
    db.commit()
    return {"detail": "Budget deleted"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.budget import Budget
from app.backend.schemas.budget_schema import BudgetCreate, BudgetRead, BudgetUpdate
from app.backend.models.user import User

router = APIRouter(prefix="/budget", tags=["budget"])


def _ensure_budget_limit(db: Session, user: User | None):
    is_premium = bool(user and user.is_premium)
    if is_premium:
        return
    user_filter = Budget.user_id == user.id if user else Budget.user_id.is_(None)
    count = db.query(Budget).filter(user_filter).count()
    if count >= settings.free_budget_limit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Free tier limited to {settings.free_budget_limit} budgets. Upgrade for more.",
        )


@router.post("", response_model=BudgetRead)
def create_budget(
    payload: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    _ensure_budget_limit(db, current_user)
    budget = Budget(
        name=payload.name,
        amount=payload.amount,
        period=payload.period,
        user_id=current_user.id if current_user else None,
    )
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.get("", response_model=list[BudgetRead])
def list_budgets(
    db: Session = Depends(get_db), current_user: User | None = Depends(get_current_user_optional)
):
    if current_user:
        return db.query(Budget).filter(Budget.user_id == current_user.id).all()
    return db.query(Budget).filter(Budget.user_id.is_(None)).all()


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    return budget


@router.put("/{budget_id}", response_model=BudgetRead)
def update_budget(
    budget_id: int,
    payload: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if current_user and budget.user_id not in (None, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(budget)
    db.commit()
    return {"detail": "Budget deleted"}


