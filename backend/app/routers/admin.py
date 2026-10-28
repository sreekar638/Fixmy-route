from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.user import User, AuditLog
from backend.app.models.route import Category, ProblemRoute, UserSearch, ResolutionStep, EvidenceRequirement, SourceReference
from backend.app.models.complaint import ComplaintRecord
from backend.app.models.feedback import RouteCorrection, UserFeedback
from backend.app.schemas.feedback import AdminStatsResponse, RouteCorrectionResponse, UserFeedbackResponse
from backend.app.services.auth_service import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Administration"])

@router.get("/stats", response_model=AdminStatsResponse)
def get_admin_stats(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_routes = db.query(func.count(ProblemRoute.id)).scalar() or 0
    verified_routes = db.query(func.count(ProblemRoute.id)).filter(ProblemRoute.verification_status == "verified").scalar() or 0
    total_searches = db.query(func.count(UserSearch.id)).scalar() or 0
    total_complaints = db.query(func.count(ComplaintRecord.id)).scalar() or 0
    pending_corrections = db.query(func.count(RouteCorrection.id)).filter(RouteCorrection.status == "pending").scalar() or 0
    feedback_count = db.query(func.count(UserFeedback.id)).scalar() or 0

    return AdminStatsResponse(
        total_users=total_users,
        total_routes=total_routes,
        verified_routes=verified_routes,
        total_searches=total_searches,
        total_complaints=total_complaints,
        pending_corrections=pending_corrections,
        feedback_count=feedback_count
    )

@router.get("/routes")
def list_admin_routes(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    routes = db.query(ProblemRoute).order_by(ProblemRoute.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "title": r.title,
            "slug": r.slug,
            "category_name": r.category.name if r.category else "None",
            "responsible_authority": r.responsible_authority,
            "verification_status": r.verification_status,
            "last_verified_at": r.last_verified_at,
            "confidence_score": r.confidence_score
        }
        for r in routes
    ]

@router.put("/routes/{id}/verification")
def update_verification_status(
    id: int,
    status_update: dict,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    route = db.query(ProblemRoute).filter(ProblemRoute.id == id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    new_status = status_update.get("verification_status", "verified")
    old_status = route.verification_status
    route.verification_status = new_status
    route.last_verified_at = datetime.utcnow()
    route.verified_by = admin.full_name

    # Audit log
    db.add(AuditLog(
        user_id=admin.id,
        action="UPDATE_ROUTE_VERIFICATION",
        target_type="problem_route",
        target_id=route.id,
        details=f"Admin changed status from '{old_status}' to '{new_status}'"
    ))
    db.commit()
    return {"message": "Route verification status updated", "new_status": new_status}

@router.get("/corrections", response_model=List[RouteCorrectionResponse])
def get_corrections(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    corrections = db.query(RouteCorrection).order_by(RouteCorrection.created_at.desc()).all()
    return corrections

@router.patch("/corrections/{id}")
def update_correction_status(
    id: int,
    patch_data: dict,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    correction = db.query(RouteCorrection).filter(RouteCorrection.id == id).first()
    if not correction:
        raise HTTPException(status_code=404, detail="Correction report not found")
    
    new_status = patch_data.get("status", "reviewed")
    admin_notes = patch_data.get("admin_notes")
    
    correction.status = new_status
    if admin_notes:
        correction.admin_notes = admin_notes
    if new_status == "resolved":
        correction.resolved_at = datetime.utcnow()

    db.add(AuditLog(
        user_id=admin.id,
        action="REVIEW_USER_CORRECTION",
        target_type="route_correction",
        target_id=correction.id,
        details=f"Status set to {new_status}. Notes: {admin_notes}"
    ))
    db.commit()
    return {"message": "Correction report updated successfully"}

@router.get("/feedback", response_model=List[UserFeedbackResponse])
def list_feedback(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    feedback_entries = db.query(UserFeedback).order_by(UserFeedback.created_at.desc()).limit(100).all()
    return feedback_entries

@router.get("/audit-logs")
def get_audit_logs(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(100).all()
    return [
        {
            "id": log.id,
            "action": log.action,
            "target_type": log.target_type,
            "target_id": log.target_id,
            "details": log.details,
            "created_at": log.created_at
        }
        for log in logs
    ]
