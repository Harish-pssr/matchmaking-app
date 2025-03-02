from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration (using SQLite as the local database)
SQLALCHEMY_DATABASE_URL = "sqlite:///./matchusers.db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()
