from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SavingGoalBase(BaseModel):
    name: str
    target_amount: float = Field(..., gt=0)
    saved_amount: float = Field(0, ge=0)
    deadline: Optional[date] = None


class SavingGoalCreate(SavingGoalBase):
    pass


class SavingGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = Field(None, gt=0)
    saved_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None


class SavingGoalRead(SavingGoalBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SavingGoalBase(BaseModel):
    name: str
    target_amount: float = Field(..., gt=0)
    saved_amount: float = Field(0, ge=0)
    deadline: Optional[date] = None


class SavingGoalCreate(SavingGoalBase):
    pass


class SavingGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = Field(None, gt=0)
    saved_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None


class SavingGoalRead(SavingGoalBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


