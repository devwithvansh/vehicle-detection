from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, cameras, dashboard, logs, ocr, vehicles
from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.bootstrap import seed_defaults

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Army vehicle detection, OCR, registration, and movement logging API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(cameras.router, prefix="/api")
app.include_router(ocr.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")


@app.on_event("startup")
def startup() -> None:
    # Ensure tables are created
    from app.db.session import Base, engine
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_defaults(db)
    finally:
        db.close()


@app.get("/health", tags=["system"])
def health():
    return {"status": "ready", "service": settings.app_name}
