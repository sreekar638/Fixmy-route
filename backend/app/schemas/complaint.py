from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class TimelineEntryCreate(BaseModel):
    status: str
    notes: str
    event_date: Optional[datetime] = None

class TimelineEntryResponse(BaseModel):
    id: int
    complaint_id: int
    status: str
    notes: str
    event_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class ChecklistItemCreate(BaseModel):
    item_title: str
    why_needed: Optional[str] = None
    is_collected: bool = False
    notes: Optional[str] = None

class ChecklistItemUpdate(BaseModel):
    is_collected: bool
    notes: Optional[str] = None

class ChecklistItemResponse(BaseModel):
    id: int
    item_title: str
    why_needed: Optional[str] = None
    is_collected: bool
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class ComplaintCreate(BaseModel):
    route_id: Optional[int] = None
    title: str
    category_name: str
    organization_name: str
    reference_number: Optional[str] = None
    official_tracking_url: Optional[str] = None
    status: str = "Submitted"
    submission_date: Optional[datetime] = None
    next_followup_date: Optional[datetime] = None
    notes: Optional[str] = None
    checklist_items: List[ChecklistItemCreate] = []

class ComplaintUpdate(BaseModel):
    title: Optional[str] = None
    organization_name: Optional[str] = None
    reference_number: Optional[str] = None
    official_tracking_url: Optional[str] = None
    status: Optional[str] = None
    next_followup_date: Optional[datetime] = None
    notes: Optional[str] = None
    resolution_summary: Optional[str] = None
    status_change_notes: Optional[str] = None  # Appended to timeline when status changes

class ComplaintResponse(BaseModel):
    id: int
    user_id: int
    route_id: Optional[int] = None
    title: str
    category_name: str
    organization_name: str
    reference_number: Optional[str] = None
    official_tracking_url: Optional[str] = None
    status: str
    submission_date: Optional[datetime] = None
    next_followup_date: Optional[datetime] = None
    notes: Optional[str] = None
    resolution_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    timeline: List[TimelineEntryResponse] = []
    checklist: List[ChecklistItemResponse] = []

    class Config:
        from_attributes = True

class ComplaintDraftGenerateRequest(BaseModel):
    route_id: Optional[int] = None
    user_name: str
    organization: str
    category: Optional[str] = None
    issue_description: str
    incident_date: Optional[str] = None
    previous_attempts: Optional[str] = None
    previous_ref_number: Optional[str] = None
    desired_resolution: str
    evidence_collected: List[str] = []
    style: str = "formal"  # "formal", "concise", "detailed"

class ComplaintDraftCreate(BaseModel):
    route_id: Optional[int] = None
    title: str
    organization: str
    recipient_authority: Optional[str] = None
    issue_description: str
    style: str = "formal"
    incident_date: Optional[str] = None
    previous_ref_number: Optional[str] = None
    desired_resolution: Optional[str] = None
    evidence_references: Optional[str] = None
    subject: str
    body: str

class ComplaintDraftResponse(BaseModel):
    id: int
    user_id: int
    route_id: Optional[int] = None
    title: str
    organization: str
    recipient_authority: Optional[str] = None
    issue_description: str
    style: str
    incident_date: Optional[str] = None
    previous_ref_number: Optional[str] = None
    desired_resolution: Optional[str] = None
    evidence_references: Optional[str] = None
    subject: str
    body: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
