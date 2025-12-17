from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.backend.core.database import Base


class AdviceLog(Base):
    __tablename__ = "advice_logs"

    id = Column(Integer, primary_key=True, index=True)
    advice_text = Column(String, nullable=False)
    severity = Column(String, default="info")
    related_budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=True)
    related_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.backend.core.database import Base


class AdviceLog(Base):
    __tablename__ = "advice_logs"

    id = Column(Integer, primary_key=True, index=True)
    advice_text = Column(String, nullable=False)
    severity = Column(String, default="info")
    related_budget_id = Column(Integer, ForeignKey("budgets.id"), nullable=True)
    related_category = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


