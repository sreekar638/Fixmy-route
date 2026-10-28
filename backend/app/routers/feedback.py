from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.feedback import UserFeedback, RouteCorrection
from backend.app.schemas.feedback import (
    UserFeedbackCreate,
    UserFeedbackResponse,
    RouteCorrectionCreate,
    RouteCorrectionResponse
)
from backend.app.services.auth_service import get_optional_current_user

router = APIRouter(prefix="/api", tags=["Feedback & Trust"])

@router.post("/feedback", response_model=UserFeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    feedback_in: UserFeedbackCreate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    feedback = UserFeedback(
        user_id=user_id,
        route_id=feedback_in.route_id,
        rating=feedback_in.rating,
        helpful=feedback_in.helpful,
        comment=feedback_in.comment,
        page_url=feedback_in.page_url
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

@router.post("/corrections", response_model=RouteCorrectionResponse, status_code=status.HTTP_201_CREATED)
def submit_correction(
    correction_in: RouteCorrectionCreate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user.id if current_user else None
    contact_email = correction_in.contact_email or (current_user.email if current_user else None)
    
    correction = RouteCorrection(
        user_id=user_id,
        route_id=correction_in.route_id,
        issue_type=correction_in.issue_type,
        details=correction_in.details,
        suggested_correction=correction_in.suggested_correction,
        source_url_suggested=correction_in.source_url_suggested,
        contact_email=contact_email,
        status="pending"
    )
    db.add(correction)
    db.commit()
    db.refresh(correction)
    return correction
