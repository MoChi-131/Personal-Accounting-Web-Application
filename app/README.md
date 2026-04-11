# App Module (Active)

This folder contains the active Flask application.

## Run
1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python flask_fyp.py`

## Important
- `flask_fyp.py` uses `MONGO_URI` environment variable if set.
- Default MongoDB URI is `mongodb://localhost:27017/`.
