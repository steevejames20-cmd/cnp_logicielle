from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdviceBase(BaseModel):
    advice_text: str
    severity: str = "info"
    related_budget_id: Optional[int] = None
    related_category: Optional[str] = None


class AdviceCreate(AdviceBase):
    pass


class AdviceRead(AdviceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdviceBase(BaseModel):
    advice_text: str
    severity: str = "info"
    related_budget_id: Optional[int] = None
    related_category: Optional[str] = None


class AdviceCreate(AdviceBase):
    pass


class AdviceRead(AdviceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


