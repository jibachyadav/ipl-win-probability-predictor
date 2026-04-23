import streamlit as st
import pickle
import pandas as pd
import numpy as np

import pickle
import os

file_path = os.path.join(os.path.dirname(__file__), "pipe.pkl")

with open(file_path, "rb") as f:
    pipe = pickle.load(f)

teams = [
    'Chennai Super Kings','Delhi Capitals',
    'Kings XI Punjab', 'Kolkata Knight Riders',
    'Mumbai Indians', 'Rajasthan Royals', 'Royal Challengers Bangalore',
    'Sunrisers Hyderabad'
]

cities = [
    'Abu Dhabi', 'Ahmedabad', 'Bangalore', 'Bengaluru', 'Bloemfontein',
    'Cape Town', 'Centurion', 'Chandigarh', 'Chennai', 'Cuttack',
    'Delhi', 'Dharamsala', 'Durban', 'East London', 'Hyderabad',
    'Indore', 'Jaipur', 'Johannesburg', 'Kanpur', 'Kimberley',
    'Kolkata', 'Mohali', 'Mumbai', 'Nagpur', 'Port Elizabeth',
    'Pune', 'Raipur', 'Rajkot', 'Ranchi', 'Sharjah', 'Visakhapatnam'
]

st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a0a1a 0%, #0f1628 50%, #0a0a1a 100%); }
.block-container { padding-top: 1.5rem; max-width: 780px; }

.header-wrap { text-align: center; padding: 1.5rem 0 0.5rem; }
.header-wrap h1 { font-size: 2.6rem; font-weight: 800; background: linear-gradient(90deg, #f5a623, #ff6b35); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; }
.header-wrap p { color: #6b7fa3; font-size: 0.95rem; margin-top: 4px; }

.section-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 1.4rem 1.6rem; margin-bottom: 1rem; }
.section-title { font-size: 0.75rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #f5a623; margin-bottom: 1rem; }

.prob-wrapper { display: flex; gap: 16px; margin-top: 1rem; }
.prob-box { flex: 1; border-radius: 16px; padding: 28px 20px; text-align: center; height: 160px; display: flex; flex-direction: column; align-items: center; justify-content: center; box-sizing: border-box; }
.prob-box-bat { background: linear-gradient(145deg, #0d2137, #0a1929); border: 2px solid #1e90ff; box-shadow: 0 0 24px rgba(30,144,255,0.15); }
.prob-box-bowl { background: linear-gradient(145deg, #1f0a0a, #150505); border: 2px solid #ff4444; box-shadow: 0 0 24px rgba(255,68,68,0.15); }
.prob-team { font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; }
.prob-team-bat { color: #7ec8f7; }
.prob-team-bowl { color: #f78e8e; }
.prob-pct { font-size: 2.8rem; font-weight: 800; line-height: 1; }
.prob-pct-bat { color: #1e90ff; }
.prob-pct-bowl { color: #ff4444; }
.prob-label { font-size: 0.7rem; color: #555; margin-top: 6px; letter-spacing: 1px; text-transform: uppercase; }

.split-bar-wrap { margin-top: 1.2rem; }
.split-bar-labels { display: flex; justify-content: space-between; font-size: 0.78rem; color: #888; margin-bottom: 6px; }
.split-bar-bg { background: rgba(255,68,68,0.25); border-radius: 8px; height: 10px; overflow: hidden; }
.split-bar-fill { height: 100%; background: linear-gradient(90deg, #1e90ff, #38bdf8); border-radius: 8px; }

div.stButton > button {
    background: linear-gradient(90deg, #f5a623, #ff6b35) !important;
    color: #0a0a1a !important; font-weight: 800 !important;
    font-size: 1rem !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 1rem !important;
    width: 100% !important;
}
div.stButton > button:hover { opacity: 0.88 !important; }
label { color: #a0aec0 !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='header-wrap'>
    <h1>🏏 IPL Win Predictor</h1>
    <p>Real-time win probability powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-card'><div class='section-title'>⚔️ Teams & Venue</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("Batting Team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Bowling Team", sorted(teams))
city = st.selectbox("Match City", sorted(cities))
st.markdown("</div>", unsafe_allow_html=True)

if batting_team == bowling_team:
    st.error("⚠️ Batting and bowling team cannot be the same!")
    st.stop()

st.markdown("<div class='section-card'><div class='section-title'>📊 Match Situation</div>", unsafe_allow_html=True)
col3, col4, col5 = st.columns(3)
with col3:
    target = st.number_input("Target Score", min_value=1, max_value=300, value=180)
with col4:
    score = st.number_input("Current Score", min_value=0, max_value=300, value=60)
with col5:
    overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=8.0, step=0.1)
wickets = st.number_input("Wickets Fallen", min_value=0, max_value=9, value=2)
st.markdown("</div>", unsafe_allow_html=True)

runs_left = target - score
balls_left = int((20 - overs) * 6)
wickets_left = 10 - wickets
crr = score / overs if overs > 0 else 0
rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

if st.button("🔮 Predict Win Probability"):
    if balls_left <= 0:
        st.error("No balls left! Match is already complete.")
    elif runs_left <= 0:
        st.success(f"🎉 {batting_team} has already won!")
    else:
        input_df = pd.DataFrame({
            'batting_team': [batting_team], 'bowling_team': [bowling_team],
            'city': [city], 'runs_left': [runs_left], 'balls_left': [balls_left],
            'wickets': [wickets_left], 'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]
        })
        result = pipe.predict_proba(input_df)
        bat_prob = round(result[0][1] * 100, 1)
        bowl_prob = round(result[0][0] * 100, 1)
        winner = batting_team if bat_prob > bowl_prob else bowling_team

        st.markdown(f"""
        <div class='section-card'>
            <div class='section-title'>🏆 Win Probability</div>
            <div class='prob-wrapper'>
                <div class='prob-box prob-box-bat'>
                    <div class='prob-team prob-team-bat'>🏏 {batting_team}</div>
                    <div class='prob-pct prob-pct-bat'>{bat_prob}%</div>
                    <div class='prob-label'>Batting</div>
                </div>
                <div class='prob-box prob-box-bowl'>
                    <div class='prob-team prob-team-bowl'>🎯 {bowling_team}</div>
                    <div class='prob-pct prob-pct-bowl'>{bowl_prob}%</div>
                    <div class='prob-label'>Bowling</div>
                </div>
            </div>
            <div class='split-bar-wrap'>
                <div class='split-bar-labels'>
                    <span style='color:#1e90ff;font-weight:600'>{batting_team}</span>
                    <span style='color:#f5a623;font-weight:700'>🏆 {winner} favored</span>
                    <span style='color:#ff4444;font-weight:600'>{bowling_team}</span>
                </div>
                <div class='split-bar-bg'>
                    <div class='split-bar-fill' style='width:{bat_prob}%'></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)