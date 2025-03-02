from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.dialects.sqlite import JSON
from database import Base
import enum

# Gender Enum

class GenderEnum(str, enum.Enum):
    """Enum for gender representation."""
    Male = "Male"
    Female = "Female"

# User Model

class User(Base):
    """SQLAlchemy model for the users table."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(Enum(GenderEnum), nullable=False)  # Uses Enum for consistency
    email = Column(String, unique=True, index=True)
    city = Column(String, index=True)
    interests = Column(JSON)  # Stores list of interests as JSON
