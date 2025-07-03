"""
Main application module for AtlanDemo.

This module demonstrates FastAPI best practices including:
- Proper application structure
- Error handling middleware
- Security configurations
- Async/await patterns
- Logging integration
- Environment-based configuration
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel

from .config.settings import get_settings
from .services.demo_service import DemoService
from .utils.error_handler import ErrorHandler
from .utils.security import SecurityManager


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    version: str
    environment: str
    timestamp: str


class DemoResponse(BaseModel):
    """Response model for demo endpoint."""
    message: str
    data: Dict[str, Any]
    success: bool


# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle events.
    
    This context manager handles startup and shutdown events,
    demonstrating proper resource management.
    """
    # Startup
    logger.info("Starting AtlanDemo application...")
    
    # Initialize services
    settings = get_settings()
    demo_service = DemoService()
    
    # Store services in app state for dependency injection
    app.state.demo_service = demo_service
    app.state.settings = settings
    
    try:
        await demo_service.initialize()
        logger.info("Application startup completed successfully")
        yield
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down AtlanDemo application...")
        await demo_service.cleanup()
        logger.info("Application shutdown completed")


# Create FastAPI application instance
app = FastAPI(
    title="AtlanDemo",
    description="A demonstration API showcasing Python best practices",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Security configuration
security_manager = SecurityManager()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling middleware
error_handler = ErrorHandler()


@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """
    Global error handling middleware.
    
    Catches and properly formats all unhandled exceptions.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return await error_handler.handle_exception(e)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """
    Security middleware for request validation and protection.
    """
    # Security headers and validation
    response = await call_next(request)
    
    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    return response


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Current application health status
    """
    from datetime import datetime
    
    return HealthResponse(
        status="healthy",
        version=app.version,
        environment=os.getenv("ENVIRONMENT", "development"),
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/", response_model=DemoResponse)
async def root() -> DemoResponse:
    """
    Root endpoint demonstrating async patterns and proper response structure.
    
    Returns:
        DemoResponse: Welcome message with application information
    """
    try:
        # Simulate async operation
        await asyncio.sleep(0.1)
        
        return DemoResponse(
            message="Welcome to AtlanDemo - A demonstration of Python best practices",
            data={
                "features": [
                    "Clean, modular architecture",
                    "Robust error handling",
                    "Security best practices",
                    "Async/await patterns",
                    "Comprehensive testing",
                    "Scalable design"
                ],
                "version": app.version,
                "docs_url": "/docs"
            },
            success=True
        )
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/demo", response_model=DemoResponse)
async def demo_endpoint(request: Request) -> DemoResponse:
    """
    Demo endpoint showcasing service layer pattern and dependency injection.
    
    Args:
        request: FastAPI request object
        
    Returns:
        DemoResponse: Demo data from service layer
    """
    try:
        # Access service from app state (dependency injection pattern)
        demo_service: DemoService = request.app.state.demo_service
        
        # Call service method (demonstrates async service pattern)
        demo_data = await demo_service.get_demo_data()
        
        return DemoResponse(
            message="Demo data retrieved successfully",
            data=demo_data,
            success=True
        )
    except Exception as e:
        logger.error(f"Error in demo endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve demo data")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom HTTP exception handler.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for all unhandled exceptions.
    
    Args:
        request: FastAPI request object
        exc: Exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "path": request.url.path
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Configure logging
    logger.remove()
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        colorize=True
    )
    
    # Get settings
    settings = get_settings()
    
    # Run application
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    ) 