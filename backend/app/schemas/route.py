from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ResolutionStepSchema(BaseModel):
    id: Optional[int] = None
    step_number: int
    title: str
    description: str
    official_url: Optional[str] = None
    action_type: str = "action"
    is_mandatory: bool = True
    warnings: Optional[str] = None

    class Config:
        from_attributes = True

class EvidenceRequirementSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    why_needed: str
    is_mandatory: bool = True
    file_type_hint: Optional[str] = "PDF, Image, or Statement"

    class Config:
        from_attributes = True

class SourceReferenceSchema(BaseModel):
    id: Optional[int] = None
    title: str
    url: str
    publisher: str
    description: Optional[str] = None
    last_checked_at: Optional[datetime] = None
    is_official: bool = True

    class Config:
        from_attributes = True

class CategorySchema(BaseModel):
    id: int
    slug: str
    name: str
    icon: str
    description: Optional[str] = None
    display_order: int = 0
    route_count: Optional[int] = 0

    class Config:
        from_attributes = True

class ProblemRouteSummary(BaseModel):
    id: int
    slug: str
    title: str
    category_id: int
    category_name: Optional[str] = None
    subcategory: Optional[str] = None
    responsible_authority: str
    authority_type: str
    reason_for_routing: str
    jurisdiction: str
    verification_status: str
    confidence_score: int
    last_verified_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ProblemRouteDetail(BaseModel):
    id: int
    slug: str
    title: str
    category_id: int
    category_name: Optional[str] = None
    subcategory: Optional[str] = None
    problem_description: str
    keywords: str
    jurisdiction: str
    applicable_states: str
    responsible_authority: str
    authority_type: str
    reason_for_routing: str
    eligibility_conditions: Optional[str] = None
    official_channel: Optional[str] = None
    official_portal_url: Optional[str] = None
    escalation_options: Optional[str] = None
    relevant_deadlines: Optional[str] = None
    verification_status: str
    last_verified_at: Optional[datetime] = None
    verified_by: Optional[str] = None
    confidence_score: int
    steps: List[ResolutionStepSchema] = []
    evidence_items: List[EvidenceRequirementSchema] = []
    sources: List[SourceReferenceSchema] = []

    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str
    category_slug: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    contacted_provider: Optional[str] = None
    incident_date: Optional[str] = None

class SearchResultItem(BaseModel):
    route: ProblemRouteSummary
    relevance_score: float
    match_reasons: List[str]
    is_verified: bool
    confidence_label: str

class SearchResponse(BaseModel):
    query: str
    detected_category: Optional[str] = None
    results: List[SearchResultItem] = []
    clarification_question: Optional[str] = None
    safe_next_step: Optional[str] = None
    total_found: int

class SavedRouteCreate(BaseModel):
    route_id: int
    notes: Optional[str] = None

class SavedRouteResponse(BaseModel):
    id: int
    route_id: int
    route_title: str
    category_name: str
    responsible_authority: str
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
