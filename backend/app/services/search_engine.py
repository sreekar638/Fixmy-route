import re
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.route import ProblemRoute, Category

# Category keyword associations for natural-language intent detection
CATEGORY_INTENTS = {
    "electricity-water": [
        "electricity", "power", "bill", "meter", "reading", "voltage", "blackout", 
        "tariff", "current", "discom", "bescom", "tneb", "msedcl", "water", "leak", 
        "water supply", "tanker", "sewage", "jal board"
    ],
    "banking-payments": [
        "bank", "atm", "money", "deducted", "transaction", "upi", "gpay", "phonepe", 
        "paytm", "account", "credit card", "debit card", "emi", "loan", "fraud", 
        "refund", "unauthorized", "chargeback", "rbi", "reversal"
    ],
    "college-university": [
        "college", "university", "degree", "marksheet", "certificate", "deposit", 
        "fee", "hostel", "ugc", "aicte", "admission", "exam", "professors", "faculty", 
        "transfer certificate", "migration certificate"
    ],
    "internet-telecom": [
        "internet", "wifi", "broadband", "fiber", "jio", "airtel", "vi", "bsnl", 
        "network", "sim", "port", "mnp", "roaming", "recharge", "speed", "down", 
        "fiber cut", "trai", "telecom"
    ],
    "housing-rental": [
        "landlord", "tenant", "rent", "deposit", "flat", "apartment", "society", 
        "rwa", "builder", "possession", "rera", "broker", "maintenance", "eviction", 
        "water leak"
    ],
    "consumer-complaints": [
        "amazon", "flipkart", "product", "defective", "warranty", "order", "delivery", 
        "return", "scam", "seller", "replacement", "e-commerce", "damaged", "repair", 
        "customer care", "guarantee"
    ],
    "workplace-problems": [
        "salary", "unpaid", "wages", "employer", "boss", "pf", "provident fund", 
        "epfo", "resignation", "notice period", "gratuity", "harassment", "termination", 
        "labour", "employment"
    ],
    "transport-public": [
        "rto", "driving licence", "dl", "rc", "challan", "traffic", "pothole", 
        "bus", "metro", "railway", "train", "irctc", "flight", "airline", "cab", "ola", "uber"
    ],
    "government-services": [
        "aadhaar", "pan card", "passport", "voter id", "ration card", "pension", 
        "certificate", "caste", "income certificate", "government", "cpgrams", "municipality"
    ],
    "cybercrime-fraud": [
        "cyber", "scam", "hacked", "phishing", "otp", "stolen", "crypto", "blackmail", 
        "identity theft", "1930", "cybercrime"
    ]
}

def detect_category_from_query(query: str) -> Optional[str]:
    query_lower = query.lower()
    scores: Dict[str, int] = {}
    for cat_slug, keywords in CATEGORY_INTENTS.items():
        score = 0
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                score += 2
            elif kw in query_lower:
                score += 1
        if score > 0:
            scores[cat_slug] = score
    if scores:
        return max(scores, key=scores.get)
    return None

def compute_relevance_score(
    route: ProblemRoute, 
    query_words: List[str], 
    target_category_slug: Optional[str] = None,
    user_state: Optional[str] = None
) -> (float, List[str]):
    score = 0.0
    reasons = []

    text_to_search = f"{route.title} {route.problem_description} {route.keywords} {route.responsible_authority}".lower()
    
    # 1. Category alignment
    if target_category_slug and route.category and route.category.slug == target_category_slug:
        score += 35.0
        reasons.append(f"Matches category '{route.category.name}'")

    # 2. Keyword exact matches
    route_keywords = [k.strip().lower() for k in route.keywords.split(",") if k.strip()]
    matched_kws = []
    for word in query_words:
        if len(word) < 3:
            continue
        if word in route_keywords:
            score += 15.0
            matched_kws.append(word)
        elif word in text_to_search:
            score += 8.0
            matched_kws.append(word)

    if matched_kws:
        reasons.append(f"Matched key terms: {', '.join(set(matched_kws[:4]))}")

    # 3. Location / Jurisdiction checks
    if user_state:
        user_state_clean = user_state.strip().lower()
        applicable = route.applicable_states.lower()
        if applicable == "all" or route.jurisdiction.lower() == "all india":
            score += 5.0
            reasons.append(f"Valid nationwide across India including {user_state.title()}")
        elif user_state_clean in applicable:
            score += 25.0
            reasons.append(f"Specifically designated for {user_state.title()}")
        else:
            # If route is for another specific state, penalize slightly
            score -= 10.0

    # 4. Verification credibility boost
    if route.verification_status == "verified":
        score += 10.0
        reasons.append("Editorial verification confirmed by FixRoute team")
    elif route.verification_status == "outdated":
        score -= 15.0
    elif route.verification_status == "disputed":
        score -= 20.0

    return max(0.0, score), reasons

def search_routes(
    db: Session,
    query: str,
    category_slug: Optional[str] = None,
    state: Optional[str] = None,
    city: Optional[str] = None,
    contacted_provider: Optional[str] = None
) -> Dict[str, Any]:
    cleaned_query = query.strip()
    words = [w.lower() for w in re.findall(r'\b\w+\b', cleaned_query)]
    
    detected_category = category_slug or detect_category_from_query(cleaned_query)
    
    routes_query = db.query(ProblemRoute)
    all_routes = routes_query.all()
    
    scored_items = []
    for route in all_routes:
        relevance, match_reasons = compute_relevance_score(
            route=route,
            query_words=words,
            target_category_slug=detected_category,
            user_state=state
        )
        if relevance > 10.0:
            confidence = "High" if relevance >= 50.0 else ("Moderate" if relevance >= 25.0 else "General Guidance")
            scored_items.append({
                "route": route,
                "relevance_score": round(relevance, 1),
                "match_reasons": match_reasons,
                "is_verified": route.verification_status == "verified",
                "confidence_label": confidence
            })

    # Sort descending by relevance score
    scored_items.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Clarification logic if query is short or ambiguous
    clarification_question = None
    safe_next_step = None

    if len(words) < 3 and not category_slug:
        clarification_question = "Could you tell us a bit more about what occurred? For example: What organization or service was involved, and what action did you request?"
        safe_next_step = "Gather any bills, receipts, or previous reference numbers while you describe the issue."
    elif not scored_items:
        clarification_question = "We couldn't locate a verified exact match for your specific query. Did you already raise a formal complaint with the primary service provider?"
        safe_next_step = "Under Indian consumer & administrative procedures, the first step is almost always serving a written notice to the provider's official grievance officer."

    return {
        "query": cleaned_query,
        "detected_category": detected_category,
        "results": scored_items,
        "clarification_question": clarification_question,
        "safe_next_step": safe_next_step,
        "total_found": len(scored_items)
    }
