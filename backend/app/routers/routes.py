from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.route import Category, ProblemRoute, SavedRoute, UserSearch
from backend.app.schemas.route import (
    CategorySchema,
    ProblemRouteDetail,
    ProblemRouteSummary,
    SavedRouteCreate,
    SavedRouteResponse
)
from backend.app.services.auth_service import get_current_user

router = APIRouter(prefix="/api", tags=["Routes & Categories"])

@router.get("/categories", response_model=List[CategorySchema])
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.display_order.asc()).all()
    results = []
    for cat in categories:
        count = db.query(func.count(ProblemRoute.id)).filter(ProblemRoute.category_id == cat.id).scalar()
        results.append(CategorySchema(
            id=cat.id,
            slug=cat.slug,
            name=cat.name,
            icon=cat.icon,
            description=cat.description,
            display_order=cat.display_order,
            route_count=count or 0
        ))
    return results

@router.get("/categories/{slug}")
def get_category_by_slug(slug: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.slug == slug).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    routes = db.query(ProblemRoute).filter(ProblemRoute.category_id == category.id).all()
    route_summaries = []
    for r in routes:
        route_summaries.append({
            "id": r.id,
            "slug": r.slug,
            "title": r.title,
            "subcategory": r.subcategory,
            "responsible_authority": r.responsible_authority,
            "authority_type": r.authority_type,
            "reason_for_routing": r.reason_for_routing,
            "jurisdiction": r.jurisdiction,
            "verification_status": r.verification_status,
            "confidence_score": r.confidence_score,
            "last_verified_at": r.last_verified_at
        })

    return {
        "id": category.id,
        "slug": category.slug,
        "name": category.name,
        "icon": category.icon,
        "description": category.description,
        "routes": route_summaries
    }

@router.get("/routes/{id_or_slug}", response_model=ProblemRouteDetail)
def get_route_detail(id_or_slug: str, db: Session = Depends(get_db)):
    if id_or_slug.isdigit():
        route = db.query(ProblemRoute).filter(ProblemRoute.id == int(id_or_slug)).first()
    else:
        route = db.query(ProblemRoute).filter(ProblemRoute.slug == id_or_slug).first()

    if not route:
        raise HTTPException(status_code=404, detail="Problem resolution route not found")

    cat_name = route.category.name if route.category else "General"
    
    return ProblemRouteDetail(
        id=route.id,
        slug=route.slug,
        title=route.title,
        category_id=route.category_id,
        category_name=cat_name,
        subcategory=route.subcategory,
        problem_description=route.problem_description,
        keywords=route.keywords,
        jurisdiction=route.jurisdiction,
        applicable_states=route.applicable_states,
        responsible_authority=route.responsible_authority,
        authority_type=route.authority_type,
        reason_for_routing=route.reason_for_routing,
        eligibility_conditions=route.eligibility_conditions,
        official_channel=route.official_channel,
        official_portal_url=route.official_portal_url,
        escalation_options=route.escalation_options,
        relevant_deadlines=route.relevant_deadlines,
        verification_status=route.verification_status,
        last_verified_at=route.last_verified_at,
        verified_by=route.verified_by,
        confidence_score=route.confidence_score,
        steps=route.steps,
        evidence_items=route.evidence_items,
        sources=route.sources
    )

# Saved Routes (Authenticated)
@router.get("/saved-routes", response_model=List[SavedRouteResponse])
def get_saved_routes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = db.query(SavedRoute).filter(SavedRoute.user_id == current_user.id).order_by(SavedRoute.created_at.desc()).all()
    results = []
    for s in saved:
        r = s.route
        results.append(SavedRouteResponse(
            id=s.id,
            route_id=s.route_id,
            route_title=r.title if r else "Route Removed",
            category_name=r.category.name if r and r.category else "General",
            responsible_authority=r.responsible_authority if r else "Unknown",
            notes=s.notes,
            created_at=s.created_at
        ))
    return results

@router.post("/saved-routes", response_model=SavedRouteResponse)
def save_route(item: SavedRouteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    route = db.query(ProblemRoute).filter(ProblemRoute.id == item.route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    
    existing = db.query(SavedRoute).filter(SavedRoute.user_id == current_user.id, SavedRoute.route_id == item.route_id).first()
    if existing:
        return SavedRouteResponse(
            id=existing.id,
            route_id=existing.route_id,
            route_title=route.title,
            category_name=route.category.name if route.category else "General",
            responsible_authority=route.responsible_authority,
            notes=existing.notes,
            created_at=existing.created_at
        )

    new_saved = SavedRoute(
        user_id=current_user.id,
        route_id=item.route_id,
        notes=item.notes
    )
    db.add(new_saved)
    db.commit()
    db.refresh(new_saved)

    return SavedRouteResponse(
        id=new_saved.id,
        route_id=new_saved.route_id,
        route_title=route.title,
        category_name=route.category.name if route.category else "General",
        responsible_authority=route.responsible_authority,
        notes=new_saved.notes,
        created_at=new_saved.created_at
    )

@router.delete("/saved-routes/{id}")
def unsave_route(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = db.query(SavedRoute).filter(SavedRoute.id == id, SavedRoute.user_id == current_user.id).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved route not found")
    db.delete(saved)
    db.commit()
    return {"message": "Route removed from saved list"}

# User Search History
@router.get("/user/searches")
def get_user_search_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    searches = db.query(UserSearch).filter(UserSearch.user_id == current_user.id).order_by(UserSearch.created_at.desc()).limit(30).all()
    return [
        {
            "id": s.id,
            "query_text": s.query_text,
            "category_slug": s.category_slug,
            "state": s.state,
            "result_count": s.result_count,
            "created_at": s.created_at
        }
        for s in searches
    ]

@router.delete("/user/searches")
def clear_user_search_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(UserSearch).filter(UserSearch.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Search history cleared successfully"}
