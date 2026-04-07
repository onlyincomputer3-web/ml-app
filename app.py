import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import plotly.express as px
import sqlite3



conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT,
    best_score INTEGER
)
""")
conn.commit()
# ------------------- PAGE CONFIG -------------------

st.set_page_config(
    page_title="AI Study Coach",
    page_icon="🤖",
    layout="wide"
)

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
        c.execute("SELECT * FROM users WHERE username=?", (new_user,))
        if c.fetchone():
            st.error("User already exists!")
        else:
            c.execute(
                "INSERT INTO users VALUES (?, ?, ?)",
                (new_user, new_pass, 0)
            )
            conn.commit()
            st.success("Account created!")

elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
    
       c.execute(
    
    
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = c.fetchone()

    if user:
        st.session_state.logged_in = True
        st.session_state.current_user = username
        st.success("Logged in!")
    else:
        st.error("Invalid credentials")

score = 75  # example score for demonstration

progress_bar = st.progress(0)

for i in range(score):
    progress_bar.progress(i + 1)

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

predict_btn = st.button("Predict Performance")

if predict_btn:
    with st.spinner("🤖 AI is analyzing your performance..."):
        import time
        time.sleep(2)   # fake delay (feels like real AI)

        prediction = model.predict([[new_hours, new_sleep, new_practice]])
        score = int(prediction[0])
    # Feedback
    if prediction[0] >= 85:
        st.success("🔥 Excellent performance!")
    elif prediction[0] >= 60:
        st.info("👍 Good, keep improving!")
    else:
        st.warning("📉 Need more effort!")
  
prediction = model.predict([[new_hours, new_sleep, new_practice]])

score = int(prediction[0])

user = st.session_state.current_user

# Update best score
user = st.session_state.current_user

if user != "":
    c.execute("SELECT best_score FROM users WHERE username=?", (user,))
    result = c.fetchone()

    if result is not None:
        current_best = result[0]

        if score > current_best:
            c.execute(
                "UPDATE users SET best_score=? WHERE username=?",
                (score, user)
            )
            conn.commit()
    else:
        st.error("User not found in database")



# AI Advice
st.subheader("🧠 AI Study Advice")

if score >= 85:
    st.success("🔥 You're doing excellent! Keep your routine consistent.")
elif score >= 60:
    st.info("👍 You're doing good, but can improve.")

    if new_hours < 6:
        st.write("📚 Increase study hours")
    if new_sleep < 7:
        st.write("😴 Improve your sleep schedule")
    if new_practice < 50:
        st.write("📝 Practice more questions")

else:
    st.warning("📉 You need improvement!")

    st.write("👉 Study at least 6-8 hours")
    st.write("👉 Sleep properly (7-8 hours)")
    st.write("👉 Practice daily questions")

score = int(prediction[0])

st.markdown(f"## 🎯 Predicted Marks: {score}")

target = st.slider("🎯 Set your target marks", 50, 100, 80)

if st.button("How to reach target"):
    if score >= target:
        st.success("You are already on track! 🎉")
    else:
        needed = target - score
        st.warning(f"You need {needed} more marks")

        st.write("💡 Suggested improvements:")
        st.write("➡ Increase study hours by 1-2 hours")
        st.write("➡ Add more practice questions")
        st.write("➡ Maintain consistent sleep")

if st.button("📅 Generate Study Plan"):
    st.subheader("Your Daily Plan")

    st.write("📚 Study: 6-8 hours")
    st.write("😴 Sleep: 7-8 hours")
    st.write("📝 Practice: 50+ questions")

    st.write("⏰ Schedule:")
    st.write("Morning: Study concepts")
    st.write("Afternoon: Practice questions")
    st.write("Evening: Revision")

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
user = st.session_state.current_user

st.subheader("📜 Your Prediction History")

if user != "":
    c.execute(
        "SELECT score FROM history WHERE username=? ORDER BY id DESC",
        (user,)
    )
    rows = c.fetchall()

    if rows:
        scores = [row[0] for row in rows]
        st.write(scores)
    else:
        st.info("No history yet")
else:
    st.warning("Please login first")


    st.markdown("""
<style>
.glow {
    text-align: center;
    font-size: 40px;
    color: #00F5A0;
    text-shadow: 0 0 10px #00F5A0, 0 0 20px #00F5A0;
}
</style>
""", unsafe_allow_html=True)
    
    st.markdown(f"<div class='glow'>🎯 {score} Marks</div>", unsafe_allow_html=True)




    st.subheader("🏆 Leaderboard")

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    score INTEGER
)
""")
conn.commit()

c.execute(
    "INSERT INTO history (username, score) VALUES (?, ?)",
    (st.session_state.current_user, int(prediction[0]))
)
conn.commit()

# Collect users and scores
st.subheader("🏆 Leaderboard")

c.execute("SELECT username, best_score FROM users ORDER BY best_score DESC")
data = c.fetchall()

for i, (user, score) in enumerate(data[:5], start=1):
    if i == 1:
        st.write(f"🥇 {user} — {score}")
    elif i == 2:
        st.write(f"🥈 {user} — {score}")
    elif i == 3:
        st.write(f"🥉 {user} — {score}")
    else:
        st.write(f"{i}. {user} — {score}")


        st.markdown(f"""
### 🎯 Your Score: {score}

📊 Rank: Top {100 - score}% students  
🔥 Performance Level: {'Elite' if score > 85 else 'Average' if score > 60 else 'Needs Work'}

📢 Share this with your friends and compare!
""")




target = st.slider("🎯 Beat this score challenge", 50, 100, 80)

if score > target:
    st.success("🔥 You beat the challenge! Share this win 💪")
else:
    st.warning("😈 Try again and beat the challenge")


    st.subheader("🏆 Top Performers")

c.execute("SELECT username, best_score FROM users ORDER BY best_score DESC LIMIT 5")
top_users = c.fetchall()

for i, user in enumerate(top_users, 1):
    st.write(f"{i}. {user[0]} — {user[1]} marks")


    st.info("📸 Screenshot your score and share on WhatsApp/Instagram!")

st.info("👥 Compare your score with friends and see who studies smarter!")
