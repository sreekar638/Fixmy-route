from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from backend.app.database import Base

class RouteCorrection(Base):
    __tablename__ = "route_corrections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=False)
    
    # "incorrect_routing", "broken_link", "outdated_info", "missing_steps", "other"
    issue_type = Column(String(100), nullable=False)
    details = Column(Text, nullable=False)
    suggested_correction = Column(Text, nullable=True)
    source_url_suggested = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    
    status = Column(String(50), default="pending")  # "pending", "reviewed", "resolved", "rejected"
    admin_notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="SET NULL"), nullable=True)
    
    rating = Column(Integer, default=5)  # 1 to 5
    helpful = Column(Boolean, default=True)
    comment = Column(Text, nullable=True)
    page_url = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
