from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.complaint import ComplaintDraft
from backend.app.schemas.complaint import (
    ComplaintDraftGenerateRequest,
    ComplaintDraftCreate,
    ComplaintDraftResponse
)
from backend.app.services.complaint_gen import generate_complaint_letter
from backend.app.services.auth_service import get_current_user, get_optional_current_user

router = APIRouter(prefix="/api/complaint-drafts", tags=["Complaint Generator"])

@router.post("/generate")
def generate_draft(request: ComplaintDraftGenerateRequest):
    result = generate_complaint_letter(
        user_name=request.user_name,
        organization=request.organization,
        category=request.category,
        issue_description=request.issue_description,
        incident_date=request.incident_date,
        previous_attempts=request.previous_attempts,
        previous_ref_number=request.previous_ref_number,
        desired_resolution=request.desired_resolution,
        evidence_collected=request.evidence_collected,
        style=request.style
    )
    return result

@router.get("", response_model=List[ComplaintDraftResponse])
def list_user_drafts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    drafts = db.query(ComplaintDraft).filter(ComplaintDraft.user_id == current_user.id).order_by(ComplaintDraft.updated_at.desc()).all()
    return drafts

@router.post("", response_model=ComplaintDraftResponse, status_code=status.HTTP_201_CREATED)
def save_draft(draft_in: ComplaintDraftCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_draft = ComplaintDraft(
        user_id=current_user.id,
        route_id=draft_in.route_id,
        title=draft_in.title,
        organization=draft_in.organization,
        recipient_authority=draft_in.recipient_authority,
        issue_description=draft_in.issue_description,
        style=draft_in.style,
        incident_date=draft_in.incident_date,
        previous_ref_number=draft_in.previous_ref_number,
        desired_resolution=draft_in.desired_resolution,
        evidence_references=draft_in.evidence_references,
        subject=draft_in.subject,
        body=draft_in.body
    )
    db.add(new_draft)
    db.commit()
    db.refresh(new_draft)
    return new_draft

@router.get("/{id}", response_model=ComplaintDraftResponse)
def get_draft(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    draft = db.query(ComplaintDraft).filter(ComplaintDraft.id == id, ComplaintDraft.user_id == current_user.id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    return draft

@router.delete("/{id}")
def delete_draft(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    draft = db.query(ComplaintDraft).filter(ComplaintDraft.id == id, ComplaintDraft.user_id == current_user.id).first()
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")
    db.delete(draft)
    db.commit()
    return {"message": "Draft deleted successfully"}
