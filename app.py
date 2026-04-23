import streamlit as st
import pickle
import pandas as pd

# Page config
st.set_page_config(page_title="IPL Win Predictor", layout="wide")

# Teams & Cities
teams = [
    'Sunrisers Hyderabad','Mumbai Indians','Royal Challengers Bangalore',
    'Kolkata Knight Riders','Kings XI Punjab','Chennai Super Kings',
    'Rajasthan Royals','Delhi Capitals'
]

cities = [
    'Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
    'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
    'Durban','Centurion','East London','Johannesburg','Kimberley',
    'Bloemfontein','Ahmedabad','Cuttack','Nagpur','Dharamsala',
    'Visakhapatnam','Pune','Raipur','Ranchi','Abu Dhabi',
    'Sharjah','Mohali','Bengaluru'
]

# Load model
pipe = pickle.load(open('pipe.pkl', 'rb'))

# Title
st.title("🏏 IPL Win Probability Predictor")

# Team selection
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Bowling Team', sorted(teams))

# Validation
if batting_team == bowling_team:
    st.warning("⚠️ Please select different teams")

# City & target
selected_city = st.selectbox('Match City', sorted(cities))
target = st.number_input('Target Score', min_value=1, step=1)

# Match inputs
col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=0, step=1)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets_out = st.number_input('Wickets Out', min_value=0, max_value=10, step=1)

# Prediction
if st.button('Predict Probability'):

    if batting_team == bowling_team:
        st.error("❌ Teams must be different")
    else:
        runs_left = target - score
        balls_left = max(0, 120 - int(overs * 6))
        wickets_left = 10 - wickets_out

        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        # ---------------- RESULT UI ----------------
        st.subheader("📊 Winning Probability")

        col6, col7 = st.columns(2)

        with col6:
            st.markdown(f"### 🏏 {batting_team}")
            st.progress(int(win * 100))
            st.success(f"{round(win * 100)}% chance to win")

        with col7:
            st.markdown(f"### 🏏 {bowling_team}")
            st.progress(int(loss * 100))
            st.error(f"{round(loss * 100)}% chance to win")

        # Extra match insights
        st.subheader("📈 Match Insights")

        col8, col9, col10, col11 = st.columns(4)

        with col8:
            st.metric("Runs Left", runs_left)

        with col9:
            st.metric("Balls Left", balls_left)

        with col10:
            st.metric("CRR", round(crr, 2))

        with col11:
            st.metric("RRR", round(rrr, 2))