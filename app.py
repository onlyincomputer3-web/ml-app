import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import plotly.express as px

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="AI Predictor", layout="wide")

# ------------------- SESSION STATE -------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ------------------- LOGIN / SIGNUP -------------------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Signup":
    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Signup"):
        if new_user in st.session_state.users:
            st.error("User already exists!")
        else:
            st.session_state.users[new_user] = {
                "password": new_pass,
                "history": []
            }
            st.success("Account created!")

elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

# ------------------- PROTECT APP -------------------
if not st.session_state.logged_in:
    st.warning("Please login to use the app")
    st.stop()

# ------------------- MAIN APP -------------------
st.success(f"Welcome {st.session_state.current_user} 👋")

st.title("🚀 AI Performance Predictor")

# ------------------- DATA -------------------
data = pd.read_csv("data.csv")

X = data[["hours", "sleep", "practice"]]
y = data["marks"]

model = LinearRegression()
model.fit(X, y)

# ------------------- INPUT -------------------
col1, col2, col3 = st.columns(3)

with col1:
    new_hours = st.slider("📚 Study Hours", 0, 10, 1)

with col2:
    new_sleep = st.slider("😴 Sleep Hours", 0, 12, 6)

with col3:
    new_practice = st.slider("📝 Practice Questions", 0, 100, 10)

# ------------------- PREDICTION -------------------
if st.button("Predict"):
    prediction = model.predict([[new_hours, new_sleep, new_practice]])

    # Save history safely
    st.session_state.users[st.session_state.current_user]["history"].append(int(prediction[0]))

    st.markdown(f"## 🎯 Predicted Marks: {int(prediction[0])}")
    st.progress(int(prediction[0]) / 100)

    # Feedback
    if prediction[0] >= 85:
        st.success("🔥 Excellent performance!")
    elif prediction[0] >= 60:
        st.info("👍 Good, keep improving!")
    else:
        st.warning("📉 Need more effort!")

# ------------------- GRAPH -------------------
fig = px.scatter_3d(
    data,
    x="hours",
    y="sleep",
    z="marks",
    color="marks",
    title="📊 Interactive 3D Study Analysis"
)

# Add prediction point
pred = model.predict([[new_hours, new_sleep, new_practice]])

fig.add_scatter3d(
    x=[new_hours],
    y=[new_sleep],
    z=[pred[0]],
    mode='markers',
    marker=dict(size=8, color='red'),
    name="Your Prediction"
)

st.plotly_chart(fig)

# ------------------- HISTORY -------------------
st.subheader("📜 Your Prediction History")

if st.session_state.logged_in and st.session_state.current_user != "":
    st.write(st.session_state.users[st.session_state.current_user]["history"])
else:
    st.write("No history yet. Please login.")