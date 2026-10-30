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
        "/index.html",
        "/search",
        "/search.html",
        "/route-detail",
        "/route-detail.html",
        "/complaint-generator",
        "/complaint-generator.html",
        "/tracker",
        "/tracker.html",
        "/dashboard",
        "/dashboard.html",
        "/admin",
        "/admin.html",
        "/about",
        "/about.html",
        "/help",
        "/help.html",
        "/privacy",
        "/privacy.html",
        "/terms",
        "/terms.html",
    ]
    for r in routes_to_test:
        response = client.get(r)
        assert response.status_code == 200, f"Route {r} failed with {response.status_code}"
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text

def test_static_assets_served():
    assets_to_test = [
        "/css/brand.css",
        "/css/layout.css",
        "/css/components.css",
        "/js/api.js",
        "/js/nav.js",
        "/static/css/brand.css",
        "/static/css/layout.css",
        "/static/css/components.css",
        "/static/js/api.js",
        "/static/js/nav.js",
    ]
    for asset in assets_to_test:
        response = client.get(asset)
        assert response.status_code == 200, f"Asset {asset} failed with {response.status_code}"
