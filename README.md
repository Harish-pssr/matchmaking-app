# FastAPI Matchmaking App

A FastAPI-based matchmaking backend that helps users find potential matches based on common interests, age similarity, and location. This project is based on [UrbanMatch-PythonTask](https://github.com/abhishek-UM/UrbanMatch-PythonTask/tree/master) and extends its functionality with improved matchmaking logic and API enhancements.

## 🚀 Features
- **User Management**: Create, update, delete, and retrieve users.
- **Matchmaking Algorithm**: Finds best matches based on:
  - **Interests similarity** (NLP + Fuzzy Matching)
  - **Age difference scoring**
  - **City-based bonus**
- **Validation & Constraints**:
  - Opposite-gender matches only
  - Minimum match percentage threshold

## 🛠️ Tech Stack
- **FastAPI** - For API development
- **SQLAlchemy** - Database ORM
- **SQLite** - Local database storage
- **Pydantic** - Data validation
- **spaCy & RapidFuzz** - NLP-based interest matching

## 📂 Project Structure
```
fastapi-matchmaking-app/
│── database.py      # Database setup
│── models.py        # SQLAlchemy models
│── schemas.py       # Pydantic schemas & matchmaking settings
│── main.py          # FastAPI app & endpoints
│── README.md        # Project documentation
```

## 🔧 Setup & Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/Harish-pssr/matchmaking-app.git
   cd matchmaking-app
   ```

2. **Create & activate a virtual environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the FastAPI server**
   ```sh
   uvicorn main:app --reload
   ```
  
## 🎯 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/` | Get all users |
| `GET` | `/users/{user_id}` | Get user by ID |
| `PUT` | `/users/{user_id}` | Update user details |
| `DELETE` | `/users/{user_id}` | Delete a user |
| `GET` | `/users/{user_id}/matches` | Get best matches for a user |


## 📊 Match Score Calculation

The matchmaking algorithm evaluates user compatibility based on **interests, age similarity, and location**.

### **Formula**
```
Match % = (INTEREST_WEIGHT × Interest Score) 
        + (AGE_WEIGHT × Age Score) 
        + (City Bonus)
```

### **Scoring Breakdown**
- **Interests Match (60%)** → NLP & Fuzzy Matching to compare user interests.
- **Age Similarity (30%)**
  - `100%` if age difference ≤ **2 years**
  - `50%` if age difference ≤ **5 years**
  - `0%` if age difference > **5 years**
- **Same City Bonus (+10 points)** → Extra points if users are from the same city.


### **Why This Project?**
With a structured matchmaking system, this project aims to enhance meaningful connections by considering interests, age compatibility, and location factors.

**"Built with ❤️ using FastAPI to make meaningful connections happen!"** 🚀