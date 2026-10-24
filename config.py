"""
Configuration Settings for Advanced Fake Product Review Detection System
==========================================================================
Provides environment-aware configuration for Flask, SQLAlchemy, File Uploads,
Model Paths, and Security Guardrails.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Serverless environment detection (Vercel / AWS Lambda)
IS_SERVERLESS = os.environ.get('VERCEL') == '1' or bool(os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))

if IS_SERVERLESS:
    os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')

class Config:
    """Base application configuration."""
    # Security Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'reviewguard-ecom-secret-key-change-in-production-2026')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Valid for session duration
    
    # Session Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600 * 4  # 4 hours
    
    # Database Configuration (SQLite) - Use /tmp for writable SQLite on serverless
    if IS_SERVERLESS:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:////tmp/reviewguard.db')
        UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
        REPORT_FOLDER = os.environ.get('REPORT_FOLDER', '/tmp/reports')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            'DATABASE_URL', 
            f"sqlite:///{BASE_DIR / 'instance' / 'reviewguard.db'}"
        )
        UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
        REPORT_FOLDER = str(BASE_DIR / 'reports')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Limits & Paths
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    DATASET_FOLDER = str(BASE_DIR / 'dataset')
    MODEL_FOLDER = str(BASE_DIR / 'models')
    ALLOWED_EXTENSIONS = {'csv'}
    
    # Model Artifact Paths
    DECISION_TREE_MODEL_PATH = str(BASE_DIR / 'models' / 'decision_tree_model.joblib')
    ADABOOST_MODEL_PATH = str(BASE_DIR / 'models' / 'adaboost_model.joblib')
    METADATA_PATH = str(BASE_DIR / 'models' / 'training_metadata.json')
    ACTIVE_DATASET_PATH = str(BASE_DIR / 'dataset' / 'sample_reviews.csv')
    
    # Default Administrative Credentials (Configurable via Environment)
    DEFAULT_ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    DEFAULT_ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Admin@12345')
    
    # URL Analysis Security Guardrails (SSRF Protection)
    SUPPORTED_DOMAINS = [
        'flipkart.com',
        'amazon.in',
        'amazon.com',
        'books.toscrape.com',
        'quotes.toscrape.com',
        'walmart.com',
        'myntra.com',
        'demo-ecommerce-reviews.local',
        'example.com'
    ]
    URL_REQUEST_TIMEOUT = 5  # seconds
    MAX_URL_RESPONSE_BYTES = 2 * 1024 * 1024  # 2 MB max download size

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

# Mapping for environment selection
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
