import json
import logging
from typing import Dict, Any, Optional
from backend.app.config import settings

logger = logging.getLogger(__name__)

def clarify_problem_with_ai(
    problem_text: str,
    selected_category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyzes ambiguous or brief user queries and produces guided clarification questions.
    If AI provider is disabled or missing credentials, falls back gracefully to deterministic rule-based guidance.
    """
    provider = settings.AI_PROVIDER.lower()
    
    # Deterministic fallback logic
    if provider == "none" or (provider == "gemini" and not settings.GEMINI_API_KEY) or (provider == "openai" and not settings.OPENAI_API_KEY):
        return {
            "source": "rule_based_engine",
            "clarification": "To route your problem accurately, please specify: (1) The specific organization or service provider involved, (2) When the issue started, and (3) What specific outcome or refund you are seeking.",
            "suggested_actions": [
                "Select your state/city if the service is governed locally (like Electricity, Water, or Municipal services).",
                "Have your latest bill, receipt, or transaction ID ready.",
                "Verify whether you have already raised a preliminary ticket with the primary customer care."
            ],
            "ai_active": False
        }

    # If Gemini or OpenAI is configured, make the request safely
    try:
        if provider == "gemini":
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = f"""
You are the FixRoute AI assistant for India.
User Problem: "{problem_text}"
Category hint: "{selected_category or 'Not specified'}"

Task:
1. Identify missing details needed to find the exact legal or regulatory grievance authority in India.
2. Ask 2 brief, polite clarifying questions.
3. Suggest 2 essential evidence documents the user should gather.

Respond ONLY with valid JSON with keys: 'clarification' (string), 'suggested_questions' (list of strings), 'recommended_documents' (list of strings).
Do not provide formal legal advice. Never invent phone numbers.
"""
            with httpx.Client(timeout=10.0) as client:
                res = client.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
                if res.status_code == 200:
                    raw_text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                    clean_json = raw_text.strip().replace("```json", "").replace("```", "").strip()
                    data = json.loads(clean_json)
                    return {
                        "source": "gemini_ai",
                        "clarification": data.get("clarification", ""),
                        "suggested_actions": data.get("recommended_documents", []),
                        "ai_active": True
                    }
    except Exception as e:
        logger.warning(f"AI Provider call failed, reverting to rule-based fallback: {e}")

    # Fallback on any API failure
    return {
        "source": "rule_based_fallback",
        "clarification": "To route your problem accurately, please identify the service provider and whether you have an existing ticket reference number.",
        "suggested_actions": [
            "Check your invoices or online receipts for account/customer ID.",
            "Review whether 30 days have elapsed since your first official complaint."
        ],
        "ai_active": False
    }
