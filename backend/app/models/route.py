from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    icon = Column(String(100), default="folder")
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=0)

    routes = relationship("ProblemRoute", back_populates="category", cascade="all, delete-orphan")

class ProblemRoute(Base):
    __tablename__ = "problem_routes"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    title = Column(String(300), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    subcategory = Column(String(200), nullable=True)
    
    problem_description = Column(Text, nullable=False)
    keywords = Column(Text, nullable=False)  # Comma-separated or JSON string
    jurisdiction = Column(String(100), default="All India")  # "All India", "State-level", "Municipal"
    applicable_states = Column(Text, default="ALL")  # "ALL" or comma-separated state codes/names
    
    responsible_authority = Column(String(300), nullable=False)
    authority_type = Column(String(100), default="Regulator")  # Ombudsman, Tribunal, Regulator, Service Provider
    reason_for_routing = Column(Text, nullable=False)
    eligibility_conditions = Column(Text, nullable=True)
    official_channel = Column(String(300), nullable=True)
    official_portal_url = Column(String(500), nullable=True)
    escalation_options = Column(Text, nullable=True)
    relevant_deadlines = Column(Text, nullable=True)
    
    verification_status = Column(String(50), default="verified")  # "verified", "unverified", "outdated", "disputed"
    last_verified_at = Column(DateTime, default=datetime.utcnow)
    verified_by = Column(String(100), default="FixRoute Editorial Team")
    confidence_score = Column(Integer, default=95)  # 0 - 100
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="routes")
    steps = relationship("ResolutionStep", back_populates="route", cascade="all, delete-orphan", order_by="ResolutionStep.step_number")
    evidence_items = relationship("EvidenceRequirement", back_populates="route", cascade="all, delete-orphan")
    sources = relationship("SourceReference", back_populates="route", cascade="all, delete-orphan")
    saved_by = relationship("SavedRoute", back_populates="route", cascade="all, delete-orphan")

class ResolutionStep(Base):
    __tablename__ = "resolution_steps"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    official_url = Column(String(500), nullable=True)
    action_type = Column(String(100), default="action")  # gather, contact, submit, track, escalate
    is_mandatory = Column(Boolean, default=True)
    warnings = Column(Text, nullable=True)

    route = relationship("ProblemRoute", back_populates="steps")

class EvidenceRequirement(Base):
    __tablename__ = "evidence_requirements"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    description = Column(Text, nullable=True)
    why_needed = Column(Text, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    file_type_hint = Column(String(100), default="PDF, Image, or Statement")

    route = relationship("ProblemRoute", back_populates="evidence_items")

class SourceReference(Base):
    __tablename__ = "source_references"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(300), nullable=False)
    url = Column(String(500), nullable=False)
    publisher = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    last_checked_at = Column(DateTime, default=datetime.utcnow)
    is_official = Column(Boolean, default=True)

    route = relationship("ProblemRoute", back_populates="sources")

class SavedRoute(Base):
    __tablename__ = "saved_routes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("problem_routes.id", ondelete="CASCADE"), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_routes")
    route = relationship("ProblemRoute", back_populates="saved_by")

class UserSearch(Base):
    __tablename__ = "user_searches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    query_text = Column(String(500), nullable=False)
    category_slug = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    result_count = Column(Integer, default=0)
    matched_route_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="searches")
