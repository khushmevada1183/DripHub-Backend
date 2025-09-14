from fastapi import FastAPI, Request
from fastapi import HTTPException as FastAPIHTTPException
from app.core.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.routes.api import api_router
from app.db import session
from app.db.base import Base
from app.core.config import settings
from app.core.supabase_client import supabase_client
from app.core.logging_config import add_app_loggers, get_logger

add_app_loggers()
logger = get_logger()

app = FastAPI(title="DripHub Backend")

# Custom exception handler for our HTTPException
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Fallback handler for any remaining FastAPI HTTPExceptions
@app.exception_handler(FastAPIHTTPException)
async def fastapi_http_exception_handler(request: Request, exc: FastAPIHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "errors": exc.errors()}
    )

# Add CORS middleware - must be added BEFORE other middleware and routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    # create database tables (for SQLite demo)
    # This is optional and can be skipped in environments where the DB
    # is managed separately or may be unreachable during deploys.
    if not settings.SKIP_DB_INIT:
        engine = session.engine
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            # Log the error but do not prevent the application from
            # starting. In production, prefer running migrations separately.
            logger.warning("db.init_failed", error=str(e))
    else:
        logger.info("db.init_skipped")

    # Supabase health check (best-effort)
    if settings.SUPABASE_URL:
        try:
            info = await supabase_client.health_check()
            logger.info("supabase.health", **info)
        except Exception as e:
            logger.warning("supabase.unreachable", error=str(e))
    else:
        logger.info("supabase.disabled")

@app.get("/")
def read_root():
    return {"message": "DripHub backend is running"}


@app.get("/health")
def health():
    """Lightweight health endpoint for readiness/liveness checks.

    This intentionally avoids touching the database so the process can
    report healthy even when the DB is unreachable (migrations are
    performed separately via Alembic).
    """
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    """DB connectivity check. Returns 200 if a simple query succeeds, 503 otherwise."""
    try:
        # lightweight check
        db = session.SessionLocal()
        try:
            # Use a raw SQL to avoid ORM model imports and keep this check minimal
            db.execute("SELECT 1")
            return {"status": "ok", "db": "reachable"}
        finally:
            db.close()
    except Exception as e:
        logger.warning("db.health_unreachable", error=str(e))
        # Keep response lightweight and machine-readable by default
        if settings.DB_HEALTH_VERBOSE:
            return JSONResponse(status_code=503, content={"status": "unavailable", "db": "unreachable", "error": str(e)})
        return JSONResponse(status_code=503, content={"status": "unavailable", "db": "unreachable"})
