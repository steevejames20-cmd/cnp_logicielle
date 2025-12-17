from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.backend.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    payment_method = Column(String, nullable=True)
    description = Column(String, nullable=True)
    date = Column(Date, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    budget = relationship("Budget", back_populates="expenses")

from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.backend.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    payment_method = Column(String, nullable=True)
    description = Column(String, nullable=True)
    date = Column(Date, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    budget = relationship("Budget", back_populates="expenses")


