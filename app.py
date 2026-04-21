import streamlit as st
import requests

# Page config
st.set_page_config(page_title="IPL Predictor", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00adb5;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🏏 IPL Win Probability Predictor</div>', unsafe_allow_html=True)
st.markdown("---")

# Teams and cities supported by the model
TEAMS = sorted([
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Delhi Capitals'
])

CITIES = sorted([
    'Hyderabad', 'Rajkot', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata',
    'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai', 'Cape Town',
    'Port Elizabeth', 'Durban', 'Centurion', 'East London',
    'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad',
    'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune',
    'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru'
])

# Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏏 Match Details")

    batting_team = st.selectbox("Batting Team", TEAMS)
    bowling_team = st.selectbox(
        "Bowling Team",
        [t for t in TEAMS if t != batting_team]
    )
    city = st.selectbox("Venue", CITIES)

with col2:
    st.markdown("### 📊 Match Situation")

    target = st.number_input("Target", min_value=1, value=180)
    runs = st.number_input("Current Score", min_value=0, value=0)
    overs = st.number_input("Overs Completed", min_value=0.1, max_value=19.5, value=6.0, step=0.1)
    wickets = st.number_input("Wickets Out", min_value=0, max_value=9, value=0, step=1)

st.markdown("")

# Button
center = st.columns([1, 2, 1])
with center[1]:
    predict_btn = st.button("🚀 Predict Win Probability", use_container_width=True)

# Prediction
if predict_btn:
    if runs >= target:
        st.error("❌ Current score cannot be equal to or exceed the target!")
    else:
        data = {
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "city": city,
            "runs": runs,
            "overs": overs,
            "wickets": wickets,
            "target": target
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=data
            )

            if response.status_code == 200:
                result = response.json()
                prob = result["batting_win_probability"] / 100

                st.markdown("### 📈 Prediction Result")
                st.progress(int(prob * 100))

                colA, colB = st.columns(2)
                with colA:
                    st.success(f"{batting_team}: {round(prob * 100, 2)}%")
                with colB:
                    st.error(f"{bowling_team}: {round((1 - prob) * 100, 2)}%")

            else:
                st.error(f"API Error {response.status_code}: Check FastAPI server")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to FastAPI. Is the server running?")
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")