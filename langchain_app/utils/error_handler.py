"""
Error handling utilities
"""

import os
import sys
import logging
import traceback
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LOG_LEVEL, LOG_FILE


# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_error(error_message: str, exception: Exception = None):
    """Log error with optional exception details"""
    if exception:
        logger.error(f"{error_message}: {str(exception)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    else:
        logger.error(error_message)


def log_info(message: str):
    """Log info message"""
    logger.info(message)


def log_warning(message: str):
    """Log warning message"""
    logger.warning(message)


def handle_api_error(response_code: int, response_text: str = "") -> str:
    """Handle API errors and return appropriate error message"""
    error_messages = {
        400: "Bad Request - Check your input parameters",
        401: "Unauthorized - Check your API token",
        403: "Forbidden - API access denied",
        404: "Not Found - Model or endpoint not available",
        429: "Rate Limit Exceeded - Please wait and try again",
        500: "Internal Server Error - Try again later",
        503: "Service Unavailable - Model is loading or overloaded"
    }
    
    base_message = error_messages.get(response_code, f"HTTP Error {response_code}")
    
    if response_text:
        return f"{base_message}: {response_text}"
    
    return base_message


class StorySmithError(Exception):
    """Custom exception for StorySmith application errors"""
    
    def __init__(self, message: str, error_type: str = "general"):
        self.message = message
        self.error_type = error_type
        self.timestamp = datetime.now()
        super().__init__(self.message)
    
    def __str__(self):
        return f"[{self.error_type.upper()}] {self.message} (at {self.timestamp})"


class APIError(StorySmithError):
    """Exception for API-related errors"""
    
    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        super().__init__(message, "api")


class ModelError(StorySmithError):
    """Exception for model-related errors"""
    
    def __init__(self, message: str, model_name: str = None):
        self.model_name = model_name
        super().__init__(message, "model")


class ImageProcessingError(StorySmithError):
    """Exception for image processing errors"""
    
    def __init__(self, message: str, operation: str = None):
        self.operation = operation
        super().__init__(message, "image_processing")
