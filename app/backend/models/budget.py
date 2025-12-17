from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.core.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String, nullable=False, default="monthly")
    created_at = Column(DateTime, default=datetime.utcnow)

    expenses = relationship("Expense", back_populates="budget", cascade="all, delete")
    user = relationship("User", back_populates="budgets")

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.backend.core.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String, nullable=False, default="monthly")
    created_at = Column(DateTime, default=datetime.utcnow)

    expenses = relationship("Expense", back_populates="budget", cascade="all, delete")
    user = relationship("User", back_populates="budgets")


