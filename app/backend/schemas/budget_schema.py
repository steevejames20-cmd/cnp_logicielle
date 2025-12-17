from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class BudgetBase(BaseModel):
    name: str
    amount: float = Field(..., gt=0)
    period: str = Field("monthly", regex="^(daily|weekly|monthly)$")
    user_id: Optional[int] = None


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = Field(None, regex="^(daily|weekly|monthly)$")


class ExpenseInline(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime

    class Config:
        orm_mode = True


class BudgetRead(BudgetBase):
    id: int
    created_at: datetime
    expenses: List[ExpenseInline] = []

    class Config:
        orm_mode = True

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class BudgetBase(BaseModel):
    name: str
    amount: float = Field(..., gt=0)
    period: str = Field("monthly", regex="^(daily|weekly|monthly)$")
    user_id: Optional[int] = None


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    name: Optional[str] = None
    amount: Optional[float] = Field(None, gt=0)
    period: Optional[str] = Field(None, regex="^(daily|weekly|monthly)$")


class ExpenseInline(BaseModel):
    id: int
    amount: float
    category: str
    date: datetime

    class Config:
        orm_mode = True


class BudgetRead(BudgetBase):
    id: int
    created_at: datetime
    expenses: List[ExpenseInline] = []

    class Config:
        orm_mode = True


