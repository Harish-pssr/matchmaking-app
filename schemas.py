from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models import GenderEnum

# User Schemas

class UserBase(BaseModel):
    """Base schema for user details."""
    name: str
    age: int
    gender: GenderEnum
    email: EmailStr  # Ensures valid email format
    city: str
    interests: List[str]

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass  

class UserUpdate(BaseModel):
    """Schema for updating user details (partial updates allowed)."""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[GenderEnum] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    interests: Optional[List[str]] = None

class User(UserBase):
    """Schema representing a user with an ID field."""
    id: int

    class Config:
        from_attributes = True  # Enables ORM mode

# Matchmaking Schema

class MatchResponse(UserBase):
    """Schema for returning matched users with additional match details."""
    match_percent: float
    common_interests: List[str]

# Configurable Matching Parameters

# Minimum match percentage required to include a match in results
MIN_MATCH_PERCENT = 50  

# Minimum fuzzy matching score for interests to be considered a match
BEST_MATCH_FUZZ_PERCENT = 80  

# Weight distribution for the final match score calculation
INTEREST_WEIGHT = 0.6  # 60% weight for common interests
AGE_WEIGHT = 0.3       # 30% weight for age similarity
CITY_BONUS = 10        # Bonus points if users are from the same city

# Age scoring thresholds for match calculation
AGE_DIFF_FULL_SCORE = 2   # 100% match if age difference ≤ 2 years
AGE_DIFF_HALF_SCORE = 5   # 50% match if age difference ≤ 5 years
