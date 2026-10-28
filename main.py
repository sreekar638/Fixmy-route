import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.config import settings
from backend.app.database import engine, Base
from backend.app.seed_data import seed_database

# Routers
from backend.app.routers.auth import router as auth_router
from backend.app.routers.search import router as search_router
from backend.app.routers.routes import router as routes_router
from backend.app.routers.complaints import router as complaints_router
from backend.app.routers.drafts import router as drafts_router
from backend.app.routers.feedback import router as feedback_router
from backend.app.routers.admin import router as admin_router
from backend.app.routers.ai import router as ai_router

app = FastAPI(
    title=settings.APP_NAME,
    description="FixRoute: Problem-solving, complaint-routing, and resolution guidance platform for India.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list if settings.cors_origin_list else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization & initial seed on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed_database()

# Register API Routers
app.include_router(auth_router)
app.include_router(search_router)
app.include_router(routes_router)
app.include_router(complaints_router)
app.include_router(drafts_router)
app.include_router(feedback_router)
app.include_router(admin_router)
app.include_router(ai_router)

# Health Check
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "founder": settings.FOUNDER_NAME,
        "market": settings.PRIMARY_MARKET,
        "ai_active": settings.AI_PROVIDER != "none"
    }

# Mount static frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    # Clean HTML Page Routes
    @app.get("/", include_in_schema=False)
    def serve_home():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/search", include_in_schema=False)
    def serve_search():
        return FileResponse(os.path.join(frontend_dir, "search.html"))

    @app.get("/route-detail", include_in_schema=False)
    def serve_route_detail():
        return FileResponse(os.path.join(frontend_dir, "route-detail.html"))

    @app.get("/complaint-generator", include_in_schema=False)
    def serve_generator():
        return FileResponse(os.path.join(frontend_dir, "complaint-generator.html"))

    @app.get("/tracker", include_in_schema=False)
    def serve_tracker():
        return FileResponse(os.path.join(frontend_dir, "tracker.html"))

    @app.get("/dashboard", include_in_schema=False)
    def serve_dashboard():
        return FileResponse(os.path.join(frontend_dir, "dashboard.html"))

    @app.get("/admin", include_in_schema=False)
    def serve_admin():
        return FileResponse(os.path.join(frontend_dir, "admin.html"))

    @app.get("/about", include_in_schema=False)
    def serve_about():
        return FileResponse(os.path.join(frontend_dir, "about.html"))

    @app.get("/help", include_in_schema=False)
    def serve_help():
        return FileResponse(os.path.join(frontend_dir, "help.html"))

    @app.get("/privacy", include_in_schema=False)
    def serve_privacy():
        return FileResponse(os.path.join(frontend_dir, "privacy.html"))

    @app.get("/terms", include_in_schema=False)
    def serve_terms():
        return FileResponse(os.path.join(frontend_dir, "terms.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
