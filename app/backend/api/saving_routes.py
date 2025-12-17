from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.saving_goal import SavingGoal
from app.backend.models.user import User
from app.backend.schemas.saving_schema import SavingGoalCreate, SavingGoalRead, SavingGoalUpdate

router = APIRouter(prefix="/saving-goal", tags=["saving"])


def _ensure_saving_limit(db: Session, user: User | None):
    is_premium = bool(user and user.is_premium)
    if is_premium:
        return
    count = db.query(SavingGoal).count()
    if count >= settings.free_saving_goal_limit:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limited to {settings.free_saving_goal_limit} saving goal(s). Upgrade for more.",
        )


@router.post("", response_model=SavingGoalRead)
def create_saving_goal(
    payload: SavingGoalCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    _ensure_saving_limit(db, current_user)
    goal = SavingGoal(**payload.dict())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("", response_model=list[SavingGoalRead])
def list_saving_goals(db: Session = Depends(get_db)):
    return db.query(SavingGoal).all()


@router.put("/{goal_id}", response_model=SavingGoalRead)
def update_saving_goal(goal_id: int, payload: SavingGoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}")
def delete_saving_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    db.delete(goal)
    db.commit()
    return {"detail": "Saving goal deleted"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.backend.core.config import settings
from app.backend.core.database import get_db
from app.backend.core.security import get_current_user_optional
from app.backend.models.saving_goal import SavingGoal
from app.backend.models.user import User
from app.backend.schemas.saving_schema import SavingGoalCreate, SavingGoalRead, SavingGoalUpdate

router = APIRouter(prefix="/saving-goal", tags=["saving"])


def _ensure_saving_limit(db: Session, user: User | None):
    is_premium = bool(user and user.is_premium)
    if is_premium:
        return
    count = db.query(SavingGoal).count()
    if count >= settings.free_saving_goal_limit:
        raise HTTPException(
            status_code=403,
            detail=f"Free tier limited to {settings.free_saving_goal_limit} saving goal(s). Upgrade for more.",
        )


@router.post("", response_model=SavingGoalRead)
def create_saving_goal(
    payload: SavingGoalCreate,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    _ensure_saving_limit(db, current_user)
    goal = SavingGoal(**payload.dict())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("", response_model=list[SavingGoalRead])
def list_saving_goals(db: Session = Depends(get_db)):
    return db.query(SavingGoal).all()


@router.put("/{goal_id}", response_model=SavingGoalRead)
def update_saving_goal(goal_id: int, payload: SavingGoalUpdate, db: Session = Depends(get_db)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(goal, field, value)
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}")
def delete_saving_goal(goal_id: int, db: Session = Depends(get_db)):
    goal = db.query(SavingGoal).filter(SavingGoal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Saving goal not found")
    db.delete(goal)
    db.commit()
    return {"detail": "Saving goal deleted"}


