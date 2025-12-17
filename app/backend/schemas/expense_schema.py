from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    budget_id: int
    amount: float = Field(..., gt=0)
    category: str
    payment_method: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExpenseBase(BaseModel):
    budget_id: int
    amount: float = Field(..., gt=0)
    category: str
    payment_method: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseRead(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


