import os
import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_URL"] = "sqlite:///./test_frontend_serve.db"
os.environ["AI_PROVIDER"] = "none"

from main import app
from backend.app.database import engine, Base
from backend.app.seed_data import seed_database

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_frontend_serve.db"):
        try:
            os.remove("./test_frontend_serve.db")
        except Exception:
            pass

def test_frontend_routes_served():
    routes_to_test = [
        "/",
        "/search",
        "/route-detail",
        "/complaint-generator",
        "/tracker",
        "/dashboard",
        "/admin",
        "/about",
        "/help",
        "/privacy",
        "/terms",
    ]
    for r in routes_to_test:
        response = client.get(r)
        assert response.status_code == 200, f"Route {r} failed with {response.status_code}"
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text

def test_static_assets_served():
    for asset in ["/static/css/brand.css", "/static/css/layout.css", "/static/css/components.css", "/static/js/api.js", "/static/js/nav.js"]:
        response = client.get(asset)
        assert response.status_code == 200, f"Asset {asset} failed with {response.status_code}"
