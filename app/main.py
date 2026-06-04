from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from requests.exceptions import RequestException

from app.api.router import api_router
from app.utils.logger import logger
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    logger.info(f"Starting {settings.app_name} backend...")
    # Add any startup logic here (e.g., verify db connection)
    yield
    logger.info(f"Shutting down {settings.app_name} backend...")
    # Add any cleanup logic here

app = FastAPI(
    title=settings.app_name,
    description="FastAPI backend for Vedanco RevenueOS with Baserow and OpenAI integration",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Centralized Exception Handlers
@app.exception_handler(RequestException)
async def request_exception_handler(request: Request, exc: RequestException):
    """Handle generic requests exceptions (Baserow/OpenRouter)."""
    logger.error(f"External API Request Exception: {str(exc)}")
    status_code = 500
    if exc.response is not None:
        if exc.response.status_code == 404:
            status_code = 404
        elif exc.response.status_code == 400:
            status_code = 400
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": "An external API error occurred. Please check logs for details."}
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueErrors typically thrown for invalid data/state."""
    logger.error(f"Value Error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle any unexpected exceptions to prevent internal server details leak."""
    logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )

@app.get("/", tags=["Root"])
def root():
    """Root endpoint to verify API is running."""
    return {"message": f"Welcome to {settings.app_name} API"}

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
