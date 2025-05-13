# app/main.py
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time

from app.config import settings
from app.routers import customer_support, marketing, crew

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI Agents for LipaChat's Customer Support and Marketing",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customer_support.router)
app.include_router(marketing.router)
app.include_router(crew.router)

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Process the request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"- Status: {response.status_code} "
            f"- Process time: {process_time:.4f}s"
        )
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request: {request.method} {request.url.path} "
            f"- Error: {str(e)} "
            f"- Process time: {process_time:.4f}s"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Check if the API is up and running."""
    return {"status": "healthy", "version": settings.APP_VERSION}

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "AI Agents for LipaChat's Customer Support and Marketing",
    }

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )