from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.ai_service import clarify_problem_with_ai

router = APIRouter(prefix="/api/ai", tags=["AI Problem Clarification"])

class ClarifyRequest(BaseModel):
    problem_text: str
    selected_category: Optional[str] = None

@router.post("/clarify")
def clarify_problem(req: ClarifyRequest):
    return clarify_problem_with_ai(
        problem_text=req.problem_text,
        selected_category=req.selected_category
    )
