"""
Database session configuration
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create database engine with optimized SQLite configuration for FastAPI
# SQLite needs special configuration for async/multi-threaded applications
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        connect_args={
            "check_same_thread": False,  # Allow multi-threaded access
            "timeout": 20,  # Timeout for acquiring lock (seconds)
        },
        pool_pre_ping=True,  # Verify connections before using
    )
else:
    # PostgreSQL configuration with connection pooling
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=5,  # Number of connections to maintain
        max_overflow=10,  # Maximum overflow connections
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
