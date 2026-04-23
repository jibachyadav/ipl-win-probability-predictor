# 🏏 IPL Win Probability Predictor

A Machine Learning-powered web application that predicts the winning probability of IPL teams in real-time using match conditions. The app is built with Streamlit and deployed for interactive use.

---

## 🚀 Live Demo

🔗 https://ipl-win-probability-predictor-1-tjpk.onrender.com/

---

## 📌 Project Overview

This project aims to simulate real-time match prediction similar to professional cricket analytics platforms. It takes match inputs such as batting team, bowling team, runs, wickets, overs, and target to estimate win probability.

---

## 🎯 Objectives

* Predict match outcome probability using ML models
* Build an interactive web interface using Streamlit
* Demonstrate real-world sports analytics use-case
* Deploy a production-ready ML app

---

## 🧠 Machine Learning Approach

* Model Used: Logistic Regression / Random Forest (update based on your model)
* Problem Type: Binary Classification
* Features:

  * Batting Team
  * Bowling Team
  * Current Score
  * Overs Completed
  * Wickets Lost
  * Target Score
  * Runs Left
  * Balls Left
  * Current Run Rate
  * Required Run Rate

---

## 📊 Dataset

* Source: IPL historical match data
* Rows: ~10,000+
* Columns: 10+ match-related features

---

## ⚙️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* Streamlit

---

## 🖥️ Application Features

* Real-time win probability prediction
* Interactive UI
* Team selection dropdown
* Dynamic input handling
* Clean visualization

---

## 📂 Project Structure

```bash
├── app.py                # Streamlit application
├── model.pkl            # Trained ML model
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
```

---

## ▶️ How to Run Locally

```bash
git clone https://github.com/your-username/ipl-win-probability-predictor.git
cd ipl-win-probability-predictor
pip install -r requirements.txt
streamlit run app.py
```


## 🤝 Contribution

Contributions are welcome! Feel free to fork the repo and submit a pull request.

#
## ⭐ Acknowledgment

Inspired by real-world cricket analytics systems and sports data science applications.

---
