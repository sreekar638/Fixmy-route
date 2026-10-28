from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class ComplaintRecord(Base):
    __tablename__ = "complaint_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(300), nullable=False)
    category_name = Column(String(200), nullable=False)
    organization_name = Column(String(300), nullable=False)
    reference_number = Column(String(150), nullable=True, index=True)
    official_tracking_url = Column(String(500), nullable=True)
    
    # Status options per FixRoute spec:
    # "Draft", "Ready to submit", "Submitted", "Acknowledgement received", 
    # "In progress", "Additional information requested", "Resolved", "Closed", "Escalation considered"
    status = Column(String(100), default="Submitted", nullable=False)
    
    submission_date = Column(DateTime, default=datetime.utcnow, nullable=True)
    next_followup_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    resolution_summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="complaints")
    timeline = relationship("ComplaintTimeline", back_populates="complaint", cascade="all, delete-orphan", order_by="ComplaintTimeline.event_date.desc()")
    checklist = relationship("EvidenceChecklistItem", back_populates="complaint", cascade="all, delete-orphan")

class ComplaintTimeline(Base):
    __tablename__ = "complaint_timelines"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaint_records.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(100), nullable=False)
    notes = Column(Text, nullable=False)
    event_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaint = relationship("ComplaintRecord", back_populates="timeline")

class ComplaintDraft(Base):
    __tablename__ = "complaint_drafts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(300), nullable=False)
    organization = Column(String(300), nullable=False)
    recipient_authority = Column(String(300), nullable=True)
    issue_description = Column(Text, nullable=False)
    style = Column(String(50), default="formal")  # "formal", "concise", "detailed"
    
    incident_date = Column(String(100), nullable=True)
    previous_ref_number = Column(String(150), nullable=True)
    desired_resolution = Column(Text, nullable=True)
    evidence_references = Column(Text, nullable=True)
    
    subject = Column(String(400), nullable=False)
    body = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="drafts")

class EvidenceChecklistItem(Base):
    __tablename__ = "evidence_checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    complaint_id = Column(Integer, ForeignKey("complaint_records.id", ondelete="CASCADE"), nullable=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=True)
    
    item_title = Column(String(300), nullable=False)
    why_needed = Column(Text, nullable=True)
    is_collected = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="checklist_items")
    complaint = relationship("ComplaintRecord", back_populates="checklist")
