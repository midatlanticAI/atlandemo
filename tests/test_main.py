"""
Unit tests for the main application module.

This module demonstrates testing best practices including:
- Async test patterns
- Mock usage
- Test fixtures
- Comprehensive test coverage
- Error testing
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from httpx import AsyncClient
from fastapi.testclient import TestClient

from src.main import app
from src.services.demo_service import DemoService, DemoServiceError


class TestMainApplication:
    """Test class for main application functionality."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    async def async_client(self):
        """Create async test client."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "message" in data
        assert "data" in data
        assert "features" in data["data"]
    
    @pytest.mark.asyncio
    async def test_demo_endpoint(self, async_client):
        """Test demo endpoint with async client."""
        response = await async_client.get("/demo")
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "message" in data
        assert "data" in data
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get("/invalid")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_error_handling(self, async_client):
        """Test error handling middleware."""
        # This would test error scenarios
        # For now, just verify the endpoints work
        response = await async_client.get("/")
        assert response.status_code == 200


class TestDemoService:
    """Test class for DemoService functionality."""
    
    @pytest.fixture
    async def demo_service(self):
        """Create and initialize demo service."""
        service = DemoService()
        await service.initialize()
        yield service
        await service.cleanup()
    
    @pytest.mark.asyncio
    async def test_service_initialization(self):
        """Test service initialization."""
        service = DemoService()
        assert not service.initialized
        
        await service.initialize()
        assert service.initialized
        assert service.start_time is not None
        
        await service.cleanup()
        assert not service.initialized
    
    @pytest.mark.asyncio
    async def test_get_demo_data(self, demo_service):
        """Test getting demo data."""
        data = await demo_service.get_demo_data()
        
        assert isinstance(data, dict)
        assert "service_info" in data
        assert "dynamic_data" in data
        assert "cached_data" in data
        assert "metadata" in data
        
        # Verify service info
        service_info = data["service_info"]
        assert service_info["name"] == "DemoService"
        assert service_info["status"] == "active"
        assert service_info["request_count"] == 1
    
    @pytest.mark.asyncio
    async def test_process_sample_data(self, demo_service):
        """Test processing sample data."""
        input_data = {
            "name": "Test",
            "value": 42,
            "active": True
        }
        
        result = await demo_service.process_sample_data(input_data)
        
        assert isinstance(result, dict)
        assert "original_data" in result
        assert "processed_at" in result
        assert "transformations" in result
        assert "validation_results" in result
        
        # Verify transformations
        transformations = result["transformations"]
        assert transformations["keys_count"] == 3
        assert "name" in transformations["string_values"]
        assert "value" in transformations["numeric_values"]
    
    @pytest.mark.asyncio
    async def test_service_error_handling(self):
        """Test service error handling."""
        service = DemoService()
        
        # Test uninitialized service
        with pytest.raises(DemoServiceError):
            await service.get_demo_data()
        
        with pytest.raises(DemoServiceError):
            await service.process_sample_data({"test": "data"})
    
    @pytest.mark.asyncio
    async def test_invalid_input_processing(self, demo_service):
        """Test processing invalid input."""
        # Test non-dict input
        with pytest.raises(DemoServiceError):
            await demo_service.process_sample_data("invalid")
        
        # Test None input
        with pytest.raises(DemoServiceError):
            await demo_service.process_sample_data(None)
    
    @pytest.mark.asyncio
    async def test_service_health_check(self, demo_service):
        """Test service health check."""
        assert demo_service.is_healthy
        
        # Test unhealthy service
        unhealthy_service = DemoService()
        assert not unhealthy_service.is_healthy


class TestErrorHandling:
    """Test class for error handling functionality."""
    
    def test_http_error_response_format(self, client):
        """Test HTTP error response format."""
        response = client.get("/invalid")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
    
    @pytest.mark.asyncio
    async def test_async_error_handling(self, async_client):
        """Test async error handling."""
        # This would test async error scenarios
        # For now, just verify async endpoints work
        response = await async_client.get("/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_application_lifespan():
    """Test application lifespan management."""
    # This would test startup/shutdown events
    # For now, just verify basic functionality
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 