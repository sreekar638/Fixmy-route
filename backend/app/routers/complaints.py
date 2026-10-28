from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.complaint import ComplaintRecord, ComplaintTimeline, EvidenceChecklistItem
from backend.app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ChecklistItemCreate,
    ChecklistItemUpdate,
    ChecklistItemResponse,
    TimelineEntryCreate,
    TimelineEntryResponse
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/complaints", tags=["Complaint Tracking"])

@router.get("", response_model=List[ComplaintResponse])
def list_complaints(
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(ComplaintRecord).filter(ComplaintRecord.user_id == current_user.id)
    if status_filter:
        q = q.filter(ComplaintRecord.status == status_filter)
    if search:
        search_term = f"%{search.strip()}%"
        q = q.filter(
            (ComplaintRecord.title.ilike(search_term)) |
            (ComplaintRecord.organization_name.ilike(search_term)) |
            (ComplaintRecord.reference_number.ilike(search_term))
        )
    complaints = q.order_by(ComplaintRecord.created_at.desc()).all()
    return complaints

@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    sub_date = complaint_data.submission_date or datetime.utcnow()
    new_complaint = ComplaintRecord(
        user_id=current_user.id,
        route_id=complaint_data.route_id,
        title=complaint_data.title,
        category_name=complaint_data.category_name,
        organization_name=complaint_data.organization_name,
        reference_number=complaint_data.reference_number,
        official_tracking_url=complaint_data.official_tracking_url,
        status=complaint_data.status,
        submission_date=sub_date,
        next_followup_date=complaint_data.next_followup_date,
        notes=complaint_data.notes
    )
    db.add(new_complaint)
    db.flush()

    # Initial timeline entry
    initial_event = ComplaintTimeline(
        complaint_id=new_complaint.id,
        status=new_complaint.status,
        notes=f"Complaint registered on FixRoute tracker with initial status '{new_complaint.status}'.",
        event_date=sub_date
    )
    db.add(initial_event)

    # Initial checklist items
    for item in complaint_data.checklist_items:
        db.add(EvidenceChecklistItem(
            user_id=current_user.id,
            complaint_id=new_complaint.id,
            route_id=complaint_data.route_id,
            item_title=item.item_title,
            why_needed=item.why_needed,
            is_collected=item.is_collected,
            notes=item.notes
        ))

    db.commit()
    db.refresh(new_complaint)
    return new_complaint

@router.get("/{id}", response_model=ComplaintResponse)
def get_complaint(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    complaint = db.query(ComplaintRecord).filter(
        ComplaintRecord.id == id,
        ComplaintRecord.user_id == current_user.id
    ).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint record not found")
    return complaint

@router.patch("/{id}", response_model=ComplaintResponse)
def update_complaint(
    id: int,
    update_data: ComplaintUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(ComplaintRecord).filter(
        ComplaintRecord.id == id,
        ComplaintRecord.user_id == current_user.id
    ).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint record not found")

    old_status = complaint.status
    if update_data.title is not None:
        complaint.title = update_data.title
    if update_data.organization_name is not None:
        complaint.organization_name = update_data.organization_name
    if update_data.reference_number is not None:
        complaint.reference_number = update_data.reference_number
    if update_data.official_tracking_url is not None:
        complaint.official_tracking_url = update_data.official_tracking_url
    if update_data.next_followup_date is not None:
        complaint.next_followup_date = update_data.next_followup_date
    if update_data.notes is not None:
        complaint.notes = update_data.notes
    if update_data.resolution_summary is not None:
        complaint.resolution_summary = update_data.resolution_summary

    # Check if status has changed
    if update_data.status and update_data.status != old_status:
        complaint.status = update_data.status
        timeline_notes = update_data.status_change_notes or f"Status updated from '{old_status}' to '{update_data.status}'."
        db.add(ComplaintTimeline(
            complaint_id=complaint.id,
            status=update_data.status,
            notes=timeline_notes,
            event_date=datetime.utcnow()
        ))

    db.commit()
    db.refresh(complaint)
    return complaint

@router.delete("/{id}")
def delete_complaint(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    complaint = db.query(ComplaintRecord).filter(
        ComplaintRecord.id == id,
        ComplaintRecord.user_id == current_user.id
    ).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint record not found")
    
    db.delete(complaint)
    db.commit()
    return {"message": "Complaint record deleted successfully"}

# Checklist item management
@router.patch("/{complaint_id}/checklist/{item_id}", response_model=ChecklistItemResponse)
def update_checklist_item(
    complaint_id: int,
    item_id: int,
    update_data: ChecklistItemUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(EvidenceChecklistItem).filter(
        EvidenceChecklistItem.id == item_id,
        EvidenceChecklistItem.complaint_id == complaint_id,
        EvidenceChecklistItem.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    
    item.is_collected = update_data.is_collected
    if update_data.notes is not None:
        item.notes = update_data.notes
    db.commit()
    db.refresh(item)
    return item

@router.post("/{complaint_id}/checklist", response_model=ChecklistItemResponse)
def add_checklist_item(
    complaint_id: int,
    item_data: ChecklistItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    complaint = db.query(ComplaintRecord).filter(
        ComplaintRecord.id == complaint_id,
        ComplaintRecord.user_id == current_user.id
    ).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint record not found")

    new_item = EvidenceChecklistItem(
        user_id=current_user.id,
        complaint_id=complaint_id,
        route_id=complaint.route_id,
        item_title=item_data.item_title,
        why_needed=item_data.why_needed or "User-added custom supporting evidence",
        is_collected=item_data.is_collected,
        notes=item_data.notes
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
