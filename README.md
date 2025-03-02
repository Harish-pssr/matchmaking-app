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

**"Built with ❤️ using FastAPI to make meaningful connections happen!"** 🚀