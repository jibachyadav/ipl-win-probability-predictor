from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import pickle
import pandas as pd

app = FastAPI()

# Load model
model = pickle.load(open("pipe.pkl", "rb"))

VALID_TEAMS = [
 'Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals'
 
]

VALID_CITIES = [
       'Hyderabad', 'Rajkot', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata',
       'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai', 'Cape Town',
       'Port Elizabeth', 'Durban', 'Centurion', 'East London',
       'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
       'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune',
       'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali',
       'Bengaluru'
]


class InputData(BaseModel):
    batting_team: str
    bowling_team: str
    city: str
    runs: int
    overs: float
    wickets: int
    target: int

    @field_validator("batting_team", "bowling_team")
    @classmethod
    def validate_team(cls, v):
        if v not in VALID_TEAMS:
            raise ValueError(f"Invalid team: {v}")
        return v

    @field_validator("city")
    @classmethod
    def validate_city(cls, v):
        if v not in VALID_CITIES:
            raise ValueError(f"Invalid city: {v}")
        return v


@app.get("/")
def home():
    return {"message": "IPL Predictor API is running"}


@app.get("/teams")
def get_teams():
    return {"teams": VALID_TEAMS}


@app.get("/cities")
def get_cities():
    return {"cities": VALID_CITIES}


@app.post("/predict")
def predict(data: InputData):
    # Validate logical constraints
    if data.batting_team == data.bowling_team:
        raise HTTPException(status_code=400, detail="Batting and bowling team cannot be the same")
    if data.runs >= data.target:
        raise HTTPException(status_code=400, detail="Current score cannot equal or exceed target")
    if data.overs <= 0:
        raise HTTPException(status_code=400, detail="Overs must be greater than 0")

    # Feature engineering (must match training)
    runs_left = data.target - data.runs
    balls_left = (20 - data.overs) * 6
    wickets_remaining = 10 - data.wickets
    crr = data.runs / data.overs
    rrr = (runs_left / (balls_left / 6)) if balls_left > 0 else 0

    df = pd.DataFrame([{
        "batting_team": data.batting_team,
        "bowling_team": data.bowling_team,
        "city": data.city,
        "runs_left": runs_left,
        "balls_left": balls_left,
        "wickets": wickets_remaining,   # model uses wickets REMAINING, not fallen
        "total_runs_x": data.target,
        "crr": crr,
        "rrr": rrr
    }])

    prediction = model.predict_proba(df)[0][1]
    return {
        "batting_team": data.batting_team,
        "bowling_team": data.bowling_team,
        "batting_win_probability": round(float(prediction) * 100, 2),
        "bowling_win_probability": round((1 - float(prediction)) * 100, 2),
    }