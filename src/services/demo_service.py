"""
Demo service module for AtlanDemo.

This module demonstrates service layer patterns including:
- Async/await patterns
- Error handling
- Business logic separation
- Resource management
- Dependency injection compatibility
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, Any, List, Optional

from loguru import logger


class DemoServiceError(Exception):
    """Custom exception for demo service errors."""
    pass


class DemoService:
    """
    Demo service class showcasing async patterns and service layer architecture.
    
    This service demonstrates:
    - Async initialization and cleanup
    - Error handling patterns
    - Business logic separation
    - Resource management
    - Logging integration
    """
    
    def __init__(self):
        """Initialize the demo service."""
        self.initialized = False
        self.start_time: Optional[datetime] = None
        self.request_count = 0
        self._demo_data_cache: Optional[Dict[str, Any]] = None
        logger.info("DemoService instance created")
    
    async def initialize(self) -> None:
        """
        Initialize the service asynchronously.
        
        Demonstrates proper async initialization patterns and resource setup.
        
        Raises:
            DemoServiceError: If initialization fails
        """
        try:
            logger.info("Initializing DemoService...")
            
            # Simulate async initialization (e.g., database connection, external API setup)
            await asyncio.sleep(0.1)
            
            # Set up service state
            self.start_time = datetime.utcnow()
            self.initialized = True
            self.request_count = 0
            
            # Pre-load demo data
            await self._load_demo_data()
            
            logger.info("DemoService initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize DemoService: {e}")
            raise DemoServiceError(f"Service initialization failed: {e}")
    
    async def cleanup(self) -> None:
        """
        Clean up service resources.
        
        Demonstrates proper resource cleanup patterns.
        """
        try:
            logger.info("Cleaning up DemoService...")
            
            # Simulate async cleanup (e.g., closing connections, saving state)
            await asyncio.sleep(0.1)
            
            # Reset service state
            self.initialized = False
            self.start_time = None
            self._demo_data_cache = None
            
            logger.info("DemoService cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during DemoService cleanup: {e}")
            # Don't raise exceptions during cleanup to avoid masking original errors
    
    async def get_demo_data(self) -> Dict[str, Any]:
        """
        Get demonstration data with async patterns.
        
        Demonstrates:
        - Service validation
        - Async data retrieval
        - Error handling
        - Caching patterns
        - Logging
        
        Returns:
            Dict[str, Any]: Demo data
            
        Raises:
            DemoServiceError: If service is not initialized or data retrieval fails
        """
        if not self.initialized:
            raise DemoServiceError("Service not initialized")
        
        try:
            # Increment request counter
            self.request_count += 1
            
            logger.info(f"Processing demo data request #{self.request_count}")
            
            # Simulate async data processing
            await asyncio.sleep(0.05)
            
            # Generate dynamic data
            demo_data = {
                "service_info": {
                    "name": "DemoService",
                    "version": "1.0.0",
                    "status": "active",
                    "uptime_seconds": self._get_uptime_seconds(),
                    "request_count": self.request_count
                },
                "dynamic_data": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "random_number": random.randint(1, 1000),
                    "sample_list": await self._generate_sample_list(),
                    "computation_result": await self._perform_computation()
                },
                "cached_data": self._demo_data_cache,
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "processing_time_ms": 50  # Simulated processing time
                }
            }
            
            logger.info(f"Demo data generated successfully for request #{self.request_count}")
            return demo_data
            
        except Exception as e:
            logger.error(f"Error generating demo data: {e}")
            raise DemoServiceError(f"Failed to generate demo data: {e}")
    
    async def process_sample_data(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process sample data with validation and error handling.
        
        Demonstrates:
        - Input validation
        - Async processing
        - Error handling
        - Data transformation
        
        Args:
            input_data: Input data to process
            
        Returns:
            Dict[str, Any]: Processed data
            
        Raises:
            DemoServiceError: If processing fails
        """
        if not self.initialized:
            raise DemoServiceError("Service not initialized")
        
        try:
            # Validate input
            if not isinstance(input_data, dict):
                raise ValueError("Input data must be a dictionary")
            
            logger.info("Processing sample data...")
            
            # Simulate async processing
            await asyncio.sleep(0.1)
            
            # Transform data
            processed_data = {
                "original_data": input_data,
                "processed_at": datetime.utcnow().isoformat(),
                "transformations": {
                    "keys_count": len(input_data),
                    "has_nested_data": any(isinstance(v, dict) for v in input_data.values()),
                    "string_values": [k for k, v in input_data.items() if isinstance(v, str)],
                    "numeric_values": [k for k, v in input_data.items() if isinstance(v, (int, float))]
                },
                "validation_results": {
                    "is_valid": True,
                    "validation_timestamp": datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Sample data processed successfully")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing sample data: {e}")
            raise DemoServiceError(f"Failed to process sample data: {e}")
    
    async def _load_demo_data(self) -> None:
        """Load demonstration data into cache."""
        try:
            # Simulate async data loading
            await asyncio.sleep(0.05)
            
            self._demo_data_cache = {
                "static_info": {
                    "application": "AtlanDemo",
                    "purpose": "Demonstrate Python best practices",
                    "features": [
                        "Async/await patterns",
                        "Error handling",
                        "Service layer architecture",
                        "Security best practices",
                        "Comprehensive logging"
                    ]
                },
                "configuration": {
                    "cache_enabled": True,
                    "async_operations": True,
                    "error_handling": True
                },
                "loaded_at": datetime.utcnow().isoformat()
            }
            
            logger.debug("Demo data loaded into cache")
            
        except Exception as e:
            logger.error(f"Error loading demo data: {e}")
            raise
    
    async def _generate_sample_list(self) -> List[Dict[str, Any]]:
        """Generate sample list data asynchronously."""
        # Simulate async processing
        await asyncio.sleep(0.01)
        
        return [
            {
                "id": i,
                "name": f"Item {i}",
                "value": random.randint(1, 100),
                "active": random.choice([True, False])
            }
            for i in range(1, 6)
        ]
    
    async def _perform_computation(self) -> Dict[str, Any]:
        """Perform sample computation asynchronously."""
        # Simulate async computation
        await asyncio.sleep(0.02)
        
        numbers = [random.randint(1, 100) for _ in range(10)]
        
        return {
            "input_numbers": numbers,
            "sum": sum(numbers),
            "average": sum(numbers) / len(numbers),
            "max": max(numbers),
            "min": min(numbers),
            "computed_at": datetime.utcnow().isoformat()
        }
    
    def _get_uptime_seconds(self) -> int:
        """Get service uptime in seconds."""
        if not self.start_time:
            return 0
        return int((datetime.utcnow() - self.start_time).total_seconds())
    
    @property
    def is_healthy(self) -> bool:
        """Check if service is healthy."""
        return self.initialized and self.start_time is not None 