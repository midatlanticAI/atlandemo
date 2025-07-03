"""
Security utility module for AtlanDemo.

This module demonstrates security best practices including:
- Password hashing and verification
- JWT token management
- Security headers
- Input sanitization
- Rate limiting support
- Security logging
"""

import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum

from passlib.context import CryptContext
from jose import JWTError, jwt
from loguru import logger


class SecurityLevel(Enum):
    """Security levels for different operations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TokenType(Enum):
    """Token types for different purposes."""
    ACCESS = "access"
    REFRESH = "refresh"
    RESET = "reset"
    VERIFICATION = "verification"


class SecurityManager:
    """
    Comprehensive security manager for the application.
    
    Provides centralized security functionality including:
    - Password hashing and verification
    - JWT token management
    - Security headers
    - Input validation
    - Security logging
    """
    
    def __init__(self):
        # Password hashing configuration
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12  # Strong but performant
        )
        
        # Security settings
        self.token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        self.max_failed_attempts = 5
        self.lockout_duration_minutes = 15
        
        # Security tracking
        self.failed_attempts = {}
        self.security_events = []
        self.max_events_history = 200
        
        logger.info("SecurityManager initialized")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        if not password:
            raise ValueError("Password cannot be empty")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        hashed = self.pwd_context.hash(password)
        
        self._log_security_event(
            event_type="password_hash",
            severity=SecurityLevel.LOW,
            details={"password_length": len(password)}
        )
        
        return hashed
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            bool: True if password is correct
        """
        try:
            result = self.pwd_context.verify(plain_password, hashed_password)
            
            self._log_security_event(
                event_type="password_verify",
                severity=SecurityLevel.LOW,
                details={"success": result}
            )
            
            return result
            
        except Exception as e:
            self._log_security_event(
                event_type="password_verify_error",
                severity=SecurityLevel.HIGH,
                details={"error": str(e)}
            )
            return False
    
    def create_access_token(
        self,
        subject: str,
        expires_delta: Optional[timedelta] = None,
        token_type: TokenType = TokenType.ACCESS,
        additional_claims: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a JWT access token.
        
        Args:
            subject: Token subject (usually user ID)
            expires_delta: Token expiration time
            token_type: Type of token
            additional_claims: Additional claims to include
            
        Returns:
            str: JWT token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
        
        # Standard claims
        to_encode = {
            "sub": subject,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": token_type.value,
            "jti": secrets.token_urlsafe(16)  # Unique token ID
        }
        
        # Add additional claims
        if additional_claims:
            to_encode.update(additional_claims)
        
        # Get secret key (in production, use environment variable)
        secret_key = self._get_secret_key()
        
        try:
            encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
            
            self._log_security_event(
                event_type="token_created",
                severity=SecurityLevel.MEDIUM,
                details={
                    "subject": subject,
                    "token_type": token_type.value,
                    "expires_at": expire.isoformat()
                }
            )
            
            return encoded_jwt
            
        except Exception as e:
            self._log_security_event(
                event_type="token_creation_error",
                severity=SecurityLevel.HIGH,
                details={"error": str(e), "subject": subject}
            )
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Token payload if valid, None otherwise
        """
        try:
            secret_key = self._get_secret_key()
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            
            # Check token type
            token_type = payload.get("type", TokenType.ACCESS.value)
            
            self._log_security_event(
                event_type="token_verified",
                severity=SecurityLevel.LOW,
                details={
                    "subject": payload.get("sub"),
                    "token_type": token_type,
                    "expires_at": payload.get("exp")
                }
            )
            
            return payload
            
        except JWTError as e:
            self._log_security_event(
                event_type="token_verification_failed",
                severity=SecurityLevel.MEDIUM,
                details={"error": str(e)}
            )
            return None
        except Exception as e:
            self._log_security_event(
                event_type="token_verification_error",
                severity=SecurityLevel.HIGH,
                details={"error": str(e)}
            )
            return None
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.
        
        Args:
            length: Token length in bytes
            
        Returns:
            str: Secure random token
        """
        return secrets.token_urlsafe(length)
    
    def check_rate_limit(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """
        Check if an identifier is rate limited.
        
        Args:
            identifier: Identifier to check (e.g., IP address, user ID)
            max_attempts: Maximum attempts allowed
            window_minutes: Time window in minutes
            
        Returns:
            bool: True if request is allowed, False if rate limited
        """
        current_time = time.time()
        window_start = current_time - (window_minutes * 60)
        
        # Clean old attempts
        if identifier in self.failed_attempts:
            self.failed_attempts[identifier] = [
                timestamp for timestamp in self.failed_attempts[identifier]
                if timestamp > window_start
            ]
        
        # Check current attempts
        attempts = len(self.failed_attempts.get(identifier, []))
        
        if attempts >= max_attempts:
            self._log_security_event(
                event_type="rate_limit_exceeded",
                severity=SecurityLevel.HIGH,
                details={
                    "identifier": identifier,
                    "attempts": attempts,
                    "max_attempts": max_attempts
                }
            )
            return False
        
        return True
    
    def record_failed_attempt(self, identifier: str):
        """
        Record a failed authentication attempt.
        
        Args:
            identifier: Identifier for the failed attempt
        """
        current_time = time.time()
        
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = []
        
        self.failed_attempts[identifier].append(current_time)
        
        self._log_security_event(
            event_type="failed_attempt_recorded",
            severity=SecurityLevel.MEDIUM,
            details={
                "identifier": identifier,
                "total_attempts": len(self.failed_attempts[identifier])
            }
        )
    
    def clear_failed_attempts(self, identifier: str):
        """
        Clear failed attempts for an identifier.
        
        Args:
            identifier: Identifier to clear
        """
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
            
            self._log_security_event(
                event_type="failed_attempts_cleared",
                severity=SecurityLevel.LOW,
                details={"identifier": identifier}
            )
    
    def get_security_headers(self) -> Dict[str, str]:
        """
        Get security headers for HTTP responses.
        
        Returns:
            Dict[str, str]: Security headers
        """
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
        }
    
    def sanitize_input(self, input_string: str) -> str:
        """
        Sanitize input string to prevent injection attacks.
        
        Args:
            input_string: Input string to sanitize
            
        Returns:
            str: Sanitized string
        """
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ["<", ">", "\"", "'", "&", ";", "(", ")", "|", "`"]
        sanitized = input_string
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        # Limit length
        max_length = 1000
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: Email address to validate
            
        Returns:
            bool: True if email is valid
        """
        import re
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def _get_secret_key(self) -> str:
        """Get secret key for JWT signing."""
        # In production, this should come from environment variables
        return "your-secret-key-change-in-production"
    
    def _log_security_event(
        self,
        event_type: str,
        severity: SecurityLevel,
        details: Dict[str, Any]
    ):
        """Log security events for monitoring."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": severity.value,
            "details": details
        }
        
        # Log to structured logger
        if severity == SecurityLevel.CRITICAL:
            logger.critical(f"Security event: {event_type}", extra=event)
        elif severity == SecurityLevel.HIGH:
            logger.error(f"Security event: {event_type}", extra=event)
        elif severity == SecurityLevel.MEDIUM:
            logger.warning(f"Security event: {event_type}", extra=event)
        else:
            logger.info(f"Security event: {event_type}", extra=event)
        
        # Store in history
        self.security_events.append(event)
        
        # Keep history size manageable
        if len(self.security_events) > self.max_events_history:
            self.security_events.pop(0)
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        Get security statistics for monitoring.
        
        Returns:
            Dict[str, Any]: Security statistics
        """
        if not self.security_events:
            return {"total_events": 0, "event_types": {}, "severities": {}}
        
        event_types = {}
        severities = {}
        
        for event in self.security_events:
            # Count by event type
            event_type = event["event_type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Count by severity
            severity = event["severity"]
            severities[severity] = severities.get(severity, 0) + 1
        
        return {
            "total_events": len(self.security_events),
            "event_types": event_types,
            "severities": severities,
            "recent_events": self.security_events[-10:],  # Last 10 events
            "active_rate_limits": len(self.failed_attempts)
        } 