from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.models.route import UserSearch, ProblemRoute, Category
from backend.app.schemas.route import SearchRequest, SearchResponse, SearchResultItem, ProblemRouteSummary
from backend.app.services.search_engine import search_routes
from backend.app.services.auth_service import get_optional_current_user

router = APIRouter(prefix="/api/search", tags=["Problem Search"])

@router.post("", response_model=SearchResponse)
def perform_search(
    request: SearchRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    search_data = search_routes(
        db=db,
        query=request.query,
        category_slug=request.category_slug,
        state=request.state,
        city=request.city,
        contacted_provider=request.contacted_provider
    )

    formatted_results = []
    top_route_id = None
    if search_data["results"]:
        top_route_id = search_data["results"][0]["route"].id

    for item in search_data["results"]:
        route = item["route"]
        cat_name = route.category.name if route.category else "General"
        summary = ProblemRouteSummary(
            id=route.id,
            slug=route.slug,
            title=route.title,
            category_id=route.category_id,
            category_name=cat_name,
            subcategory=route.subcategory,
            responsible_authority=route.responsible_authority,
            authority_type=route.authority_type,
            reason_for_routing=route.reason_for_routing,
            jurisdiction=route.jurisdiction,
            verification_status=route.verification_status,
            confidence_score=route.confidence_score,
            last_verified_at=route.last_verified_at
        )
        formatted_results.append(SearchResultItem(
            route=summary,
            relevance_score=item["relevance_score"],
            match_reasons=item["match_reasons"],
            is_verified=item["is_verified"],
            confidence_label=item["confidence_label"]
        ))

    # Log user search if query is non-empty
    if request.query.strip():
        user_id = current_user.id if current_user else None
        db.add(UserSearch(
            user_id=user_id,
            query_text=request.query.strip()[:500],
            category_slug=request.category_slug or search_data["detected_category"],
            state=request.state,
            city=request.city,
            result_count=len(formatted_results),
            matched_route_id=top_route_id
        ))
        db.commit()

    return SearchResponse(
        query=search_data["query"],
        detected_category=search_data["detected_category"],
        results=formatted_results,
        clarification_question=search_data["clarification_question"],
        safe_next_step=search_data["safe_next_step"],
        total_found=len(formatted_results)
    )
