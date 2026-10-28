import os
import pytest
from fastapi.testclient import TestClient

# Ensure test uses an isolated in-memory or test database
os.environ["DATABASE_URL"] = "sqlite:///./test_fixroute.db"
os.environ["AI_PROVIDER"] = "none"

from main import app
from backend.app.database import engine, Base, SessionLocal
from backend.app.seed_data import seed_database
from backend.app.models.user import User

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_fixroute.db"):
        try:
            os.remove("./test_fixroute.db")
        except Exception:
            pass

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["app"] == "FixRoute"
    assert data["founder"] == "Sreekar"

def test_list_categories():
    response = client.get("/api/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 10
    slugs = [c["slug"] for c in categories]
    assert "banking-payments" in slugs
    assert "electricity-water" in slugs
    assert "college-university" in slugs

def test_natural_language_search_electricity():
    response = client.post("/api/search", json={"query": "My electricity bill is incorrect and too high"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_found"] > 0
    top = data["results"][0]
    assert "electricity" in top["route"]["title"].lower() or "discom" in top["route"]["title"].lower()
    assert top["is_verified"] is True
    assert len(top["match_reasons"]) > 0

def test_natural_language_search_banking():
    response = client.post("/api/search", json={"query": "My bank transaction failed but money was deducted from my account"})
    assert response.status_code == 200
    data = response.json()
    assert data["total_found"] > 0
    top = data["results"][0]
    assert "bank" in top["route"]["title"].lower()
    assert "rbi" in top["route"]["responsible_authority"].lower()

def test_route_detail_and_steps():
    response = client.get("/api/routes/bank-transaction-failed-money-deducted")
    assert response.status_code == 200
    route = response.json()
    assert route["title"] == "Bank Transaction Failed but Money Was Deducted (UPI / ATM / IMPS)"
    assert len(route["steps"]) >= 4
    assert len(route["evidence_items"]) >= 3
    assert len(route["sources"]) >= 2
    assert route["verification_status"] == "verified"

def test_user_registration_and_login():
    reg_payload = {
        "email": "testuser@fixroute.in",
        "full_name": "Test User India",
        "password": "Password123!"
    }
    res_reg = client.post("/api/auth/register", json=reg_payload)
    assert res_reg.status_code == 201
    reg_data = res_reg.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == "testuser@fixroute.in"

    # Login
    login_payload = {
        "email": "testuser@fixroute.in",
        "password": "Password123!"
    }
    res_login = client.post("/api/auth/login", json=login_payload)
    assert res_login.status_code == 200
    login_data = res_login.json()
    assert "access_token" in login_data
    token = login_data["access_token"]

    # Test /me
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "testuser@fixroute.in"

def test_complaint_draft_generation():
    gen_payload = {
        "user_name": "Sreekar Founder",
        "organization": "State Bank of India",
        "category": "banking-payments",
        "issue_description": "₹5,000 debited during UPI payment at supermarket, merchant received nothing.",
        "incident_date": "24 October 2026",
        "previous_attempts": "Customer care executive said to wait 72 hours.",
        "previous_ref_number": "UPI/123456789012",
        "desired_resolution": "Immediate reversal of ₹5,000 and ₹100 per day statutory delay compensation.",
        "evidence_collected": ["Account debit SMS screenshot", "Passbook statement", "Supermarket payment failure receipt"],
        "style": "formal"
    }
    response = client.post("/api/complaint-drafts/generate", json=gen_payload)
    assert response.status_code == 200
    draft = response.json()
    assert "FORMAL GRIEVANCE" in draft["subject"]
    assert "State Bank of India" in draft["body"]
    assert "₹5,000" in draft["body"]
    assert "Supermarket payment failure receipt" in draft["body"]

def test_complaint_tracking_flow():
    # Login as test user
    res_login = client.post("/api/auth/login", json={"email": "testuser@fixroute.in", "password": "Password123!"})
    token = res_login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create complaint
    create_payload = {
        "title": "Unreversed Failed UPI Debit ₹5,000",
        "category_name": "Banking and Payments",
        "organization_name": "State Bank of India",
        "reference_number": "SBI-GRIEV-99214",
        "status": "Submitted",
        "notes": "Spoke to branch manager, awaiting internal audit report.",
        "checklist_items": [
            {"item_title": "Bank Passbook Statement", "why_needed": "Shows debit", "is_collected": True},
            {"item_title": "Supermarket Merchant Slip", "why_needed": "Shows failure", "is_collected": False}
        ]
    }
    res_comp = client.post("/api/complaints", json=create_payload, headers=headers)
    assert res_comp.status_code == 201
    comp_data = res_comp.json()
    comp_id = comp_data["id"]
    assert comp_data["title"] == create_payload["title"]
    assert len(comp_data["timeline"]) == 1
    assert len(comp_data["checklist"]) == 2

    # 2. Update status to 'In progress'
    update_payload = {
        "status": "In progress",
        "status_change_notes": "Received SMS acknowledgement from SBI Grievance Officer with 7-day turnaround."
    }
    res_upd = client.patch(f"/api/complaints/{comp_id}", json=update_payload, headers=headers)
    assert res_upd.status_code == 200
    upd_data = res_upd.json()
    assert upd_data["status"] == "In progress"
    assert len(upd_data["timeline"]) == 2

    # 3. List complaints
    res_list = client.get("/api/complaints", headers=headers)
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

def test_admin_authorization_and_stats():
    # Regular user cannot access admin stats
    res_user_login = client.post("/api/auth/login", json={"email": "testuser@fixroute.in", "password": "Password123!"})
    user_token = res_user_login.json()["access_token"]
    res_forbidden = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {user_token}"})
    assert res_forbidden.status_code == 403

    # Admin user can access
    res_admin_login = client.post("/api/auth/login", json={"email": "admin@fixroute.in", "password": "AdminSecureFixRoute2026!"})
    assert res_admin_login.status_code == 200
    admin_token = res_admin_login.json()["access_token"]
    
    res_stats = client.get("/api/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert stats["total_routes"] >= 8
    assert stats["verified_routes"] >= 8

def test_feedback_and_correction_submission():
    fb_res = client.post("/api/feedback", json={
        "rating": 5,
        "helpful": True,
        "comment": "FixRoute helped me get my UPI refund credited within 2 days!"
    })
    assert fb_res.status_code == 201
    assert fb_res.json()["helpful"] is True

    corr_res = client.post("/api/corrections", json={
        "route_id": 1,
        "issue_type": "broken_link",
        "details": "The Discom portal link was updated recently.",
        "contact_email": "citizen@example.in"
    })
    assert corr_res.status_code == 201
    assert corr_res.json()["status"] == "pending"

def test_ai_clarification_fallback():
    res = client.post("/api/ai/clarify", json={"problem_text": "water leak"})
    assert res.status_code == 200
    data = res.json()
    assert "clarification" in data
    assert "suggested_actions" in data
    assert data["ai_active"] is False  # Fallback mode verified
