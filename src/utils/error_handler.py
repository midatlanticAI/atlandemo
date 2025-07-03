"""
Error handling utility module for AtlanDemo.

This module demonstrates comprehensive error handling patterns including:
- Custom exception classes
- Error logging
- Error response formatting
- Exception categorization
- Security-aware error handling
"""

import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Type
from enum import Enum

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger


class ErrorSeverity(Enum):
    """Error severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification."""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    DATABASE = "database"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class BaseAppError(Exception):
    """
    Base application error class.
    
    Provides structured error handling with categorization and severity levels.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "UNKNOWN_ERROR",
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.cause = cause
        self.timestamp = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary representation."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class ValidationError(BaseAppError):
    """Validation error for input validation failures."""
    
    def __init__(self, message: str, field: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.LOW,
            **kwargs
        )
        if field:
            self.details["field"] = field


class AuthenticationError(BaseAppError):
    """Authentication error for authentication failures."""
    
    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            category=ErrorCategory.AUTHENTICATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class AuthorizationError(BaseAppError):
    """Authorization error for authorization failures."""
    
    def __init__(self, message: str = "Access denied", **kwargs):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            category=ErrorCategory.AUTHORIZATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class BusinessLogicError(BaseAppError):
    """Business logic error for business rule violations."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code="BUSINESS_LOGIC_ERROR",
            category=ErrorCategory.BUSINESS_LOGIC,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )


class ExternalServiceError(BaseAppError):
    """External service error for external API failures."""
    
    def __init__(self, message: str, service_name: Optional[str] = None, **kwargs):
        super().__init__(
            message=message,
            error_code="EXTERNAL_SERVICE_ERROR",
            category=ErrorCategory.EXTERNAL_SERVICE,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        if service_name:
            self.details["service_name"] = service_name


class DatabaseError(BaseAppError):
    """Database error for database operation failures."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )


class SystemError(BaseAppError):
    """System error for system-level failures."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(
            message=message,
            error_code="SYSTEM_ERROR",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            **kwargs
        )


class ErrorHandler:
    """
    Comprehensive error handler for the application.
    
    Provides centralized error handling with:
    - Exception categorization
    - Logging integration
    - Security-aware error responses
    - Error metrics collection
    """
    
    def __init__(self):
        self.error_count = 0
        self.error_history = []
        self.max_history_size = 100
    
    async def handle_exception(self, exception: Exception) -> JSONResponse:
        """
        Handle exceptions and return appropriate HTTP responses.
        
        Args:
            exception: The exception to handle
            
        Returns:
            JSONResponse: Formatted error response
        """
        self.error_count += 1
        
        # Handle known application errors
        if isinstance(exception, BaseAppError):
            return await self._handle_app_error(exception)
        
        # Handle HTTP exceptions
        if isinstance(exception, HTTPException):
            return await self._handle_http_exception(exception)
        
        # Handle unknown exceptions
        return await self._handle_unknown_exception(exception)
    
    async def _handle_app_error(self, error: BaseAppError) -> JSONResponse:
        """Handle application-specific errors."""
        # Log error based on severity
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"Critical error: {error.message}", extra=error.to_dict())
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(f"High severity error: {error.message}", extra=error.to_dict())
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(f"Medium severity error: {error.message}", extra=error.to_dict())
        else:
            logger.info(f"Low severity error: {error.message}", extra=error.to_dict())
        
        # Record error in history
        self._record_error(error)
        
        # Determine HTTP status code
        status_code = self._get_status_code_for_error(error)
        
        # Create secure error response
        response_data = {
            "error": True,
            "message": error.message,
            "error_code": error.error_code,
            "category": error.category.value,
            "timestamp": error.timestamp.isoformat()
        }
        
        # Add details for non-sensitive errors
        if error.category not in [ErrorCategory.AUTHENTICATION, ErrorCategory.AUTHORIZATION]:
            response_data["details"] = error.details
        
        return JSONResponse(
            status_code=status_code,
            content=response_data
        )
    
    async def _handle_http_exception(self, exception: HTTPException) -> JSONResponse:
        """Handle FastAPI HTTP exceptions."""
        logger.warning(f"HTTP {exception.status_code}: {exception.detail}")
        
        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error": True,
                "message": exception.detail,
                "status_code": exception.status_code,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    async def _handle_unknown_exception(self, exception: Exception) -> JSONResponse:
        """Handle unknown exceptions."""
        error_id = f"error_{self.error_count}"
        
        logger.error(
            f"Unhandled exception [{error_id}]: {exception}",
            extra={
                "error_id": error_id,
                "exception_type": type(exception).__name__,
                "traceback": traceback.format_exc()
            }
        )
        
        # Record error
        self._record_error(SystemError(
            message=f"Unhandled system error: {error_id}",
            details={"exception_type": type(exception).__name__}
        ))
        
        # Return secure error response (don't expose internal details)
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Internal server error",
                "error_id": error_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    def _get_status_code_for_error(self, error: BaseAppError) -> int:
        """Get appropriate HTTP status code for error category."""
        status_map = {
            ErrorCategory.VALIDATION: 400,
            ErrorCategory.AUTHENTICATION: 401,
            ErrorCategory.AUTHORIZATION: 403,
            ErrorCategory.BUSINESS_LOGIC: 400,
            ErrorCategory.EXTERNAL_SERVICE: 502,
            ErrorCategory.DATABASE: 500,
            ErrorCategory.SYSTEM: 500,
            ErrorCategory.UNKNOWN: 500
        }
        return status_map.get(error.category, 500)
    
    def _record_error(self, error: BaseAppError):
        """Record error in history for monitoring."""
        self.error_history.append({
            "timestamp": error.timestamp,
            "error_code": error.error_code,
            "category": error.category.value,
            "severity": error.severity.value,
            "message": error.message
        })
        
        # Keep history size manageable
        if len(self.error_history) > self.max_history_size:
            self.error_history.pop(0)
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics for monitoring."""
        if not self.error_history:
            return {"total_errors": 0, "categories": {}, "severities": {}}
        
        categories = {}
        severities = {}
        
        for error in self.error_history:
            # Count by category
            category = error["category"]
            categories[category] = categories.get(category, 0) + 1
            
            # Count by severity
            severity = error["severity"]
            severities[severity] = severities.get(severity, 0) + 1
        
        return {
            "total_errors": len(self.error_history),
            "categories": categories,
            "severities": severities,
            "recent_errors": self.error_history[-5:]  # Last 5 errors
        }
    
    def clear_error_history(self):
        """Clear error history (for testing or reset)."""
        self.error_history.clear()
        self.error_count = 0 