from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
import spacy
from rapidfuzz import fuzz
from models import GenderEnum
from schemas import (
    MatchResponse, MIN_MATCH_PERCENT, INTEREST_WEIGHT, AGE_WEIGHT, 
    CITY_BONUS, AGE_DIFF_FULL_SCORE, AGE_DIFF_HALF_SCORE, BEST_MATCH_FUZZ_PERCENT
)

# Load NLP model for interest similarity comparison
nlp = spacy.load("en_core_web_md")

# Initialize FastAPI app
app = FastAPI()

# Create database tables (if they don’t exist)
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User CRUD Operations

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve a paginated list of users."""
    return db.query(models.User).offset(skip).limit(limit).all()

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieve a user by ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """Update user details (partial updates allowed)."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user by ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Matchmaking API

@app.get("/users/{user_id}/matches", response_model=list[MatchResponse])
def find_matches(user_id: int, db: Session = Depends(get_db)):
    """Find potential matches for a user based on interests, age, and location."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Find users of the opposite gender
    opposite_gender = GenderEnum.Female if user.gender == GenderEnum.Male else GenderEnum.Male
    potential_matches = db.query(models.User).filter(models.User.gender == opposite_gender).all()

    matches = []

    for match in potential_matches:
        match_score, common_interests = calculate_match_score(user, match)
        if match_score >= MIN_MATCH_PERCENT:
            matches.append(MatchResponse(
                id=match.id,
                name=match.name,
                age=match.age,
                gender=match.gender,
                email=match.email,
                city=match.city,
                interests=match.interests,
                match_percent=match_score,
                common_interests=common_interests
            ))

    return sorted(matches, key=lambda x: x.match_percent, reverse=True)

# Match Score Calculation

def calculate_match_score(user, match):
    """Calculate the match score based on interests, age, and city similarity."""
    interest_score, common_interests = get_interest_score(user.interests, match.interests)

    # Compute age similarity score
    age_diff = abs(user.age - match.age)
    if age_diff <= AGE_DIFF_FULL_SCORE:
        age_score = 100
    elif age_diff <= AGE_DIFF_HALF_SCORE:
        age_score = 50
    else:
        age_score = 0

    # City match bonus
    city_bonus = CITY_BONUS if user.city.lower() == match.city.lower() else 0

    # Final weighted match score calculation
    final_score = (INTEREST_WEIGHT * interest_score) + (AGE_WEIGHT * age_score) + city_bonus
    return round(final_score, 2), common_interests

# Interest Matching (NLP + Fuzzy Matching)

def get_interest_score(interests1, interests2):
    """Calculate interest similarity using NLP and fuzzy matching."""
    if not interests1 or not interests2:
        return 0, []  # No interests = No score

    common_interests = []
    total_score = 0
    count = 0

    for i1 in interests1:
        best_match_score = max(fuzz.ratio(i1, i2) for i2 in interests2)
        if best_match_score >= BEST_MATCH_FUZZ_PERCENT:
            common_interests.append(i1)
        total_score += best_match_score
        count += 1

    return round(total_score / count, 2) if count else 0, common_interests
