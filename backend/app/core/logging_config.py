"""Logging configuration for the Image Classification Service."""

import logging
import logging.config
from pathlib import Path
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Configure logging for the application."""
    
    # Create date-based directory structure
    date_str = datetime.now().strftime('%Y%m%d')
    date_log_dir = LOG_DIR / date_str
    date_log_dir.mkdir(exist_ok=True)
    
    # Generate log filenames
    log_filename = f"application.log"
    classification_log_filename = f"classification.log"
    error_log_filename = f"errors.log"
    
    log_path = date_log_dir / log_filename
    classification_log_path = date_log_dir / classification_log_filename
    error_log_path = date_log_dir / error_log_filename
    
    # Logging configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
            'classification': {
                'format': '%(asctime)s [CLASSIFICATION] %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': str(log_path),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'classification_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'classification',
                'filename': str(classification_log_path),
                'maxBytes': 5242880,  # 5MB
                'backupCount': 3,
                'encoding': 'utf8'
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': str(error_log_path),
                'maxBytes': 5242880,  # 5MB
                'backupCount': 3,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            '': {  # Root logger
                'handlers': ['console', 'file', 'error_file'],
                'level': 'INFO',
                'propagate': False
            },
            'app.api.routes.classification': {
                'handlers': ['console', 'file', 'classification_file', 'error_file'],
                'level': 'INFO',
                'propagate': False
            },
            'app.services.classification_service': {
                'handlers': ['console', 'file', 'classification_file', 'error_file'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': False
            },
            'uvicorn.access': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log setup completion
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured. Date folder: {date_log_dir.absolute()}")
    logger.info(f"Application log: {log_path}")
    logger.info(f"Classification log: {classification_log_path}")
    logger.info(f"Error log: {error_log_path}")
    
    return logger

def get_classification_logger():
    """Get a specialized logger for classification operations."""
    return logging.getLogger('app.api.routes.classification')