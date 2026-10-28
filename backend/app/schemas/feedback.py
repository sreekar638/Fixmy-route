from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class RouteCorrectionCreate(BaseModel):
    route_id: int
    issue_type: str  # "incorrect_routing", "broken_link", "outdated_info", "missing_steps", "other"
    details: str
    suggested_correction: Optional[str] = None
    source_url_suggested: Optional[str] = None
    contact_email: Optional[EmailStr] = None

class RouteCorrectionResponse(BaseModel):
    id: int
    route_id: int
    issue_type: str
    details: str
    suggested_correction: Optional[str] = None
    source_url_suggested: Optional[str] = None
    contact_email: Optional[str] = None
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserFeedbackCreate(BaseModel):
    route_id: Optional[int] = None
    rating: int = 5
    helpful: bool = True
    comment: Optional[str] = None
    page_url: Optional[str] = None

class UserFeedbackResponse(BaseModel):
    id: int
    route_id: Optional[int] = None
    rating: int
    helpful: bool
    comment: Optional[str] = None
    page_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AdminStatsResponse(BaseModel):
    total_users: int
    total_routes: int
    verified_routes: int
    total_searches: int
    total_complaints: int
    pending_corrections: int
    feedback_count: int
