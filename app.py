from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt      

if "history" not in st.session_state:
    st.session_state.history = []


st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input")

with col2:
    st.subheader("Output")

st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Center everything */
.block-container {
    padding-top: 2rem;
    text-align: center;
}

/* Glass box */
.css-1d391kg {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

/* Buttons */
.stButton>button {
    background-color: #ff4b2b;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
}

/* Slider */
.stSlider {
    color: white;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="AI Marks Predictor", page_icon="🤖", layout="centered")

# Title:

st.markdown("""
<h1 style='text-align: center; color: #00F5A0;'>
🚀 AI Performance Predictor
</h1>
<p style='text-align: center; font-size:18px;'>
Smart analysis of your study habits using Machine Learning 🤖
</p>
""", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Input Your Data")

# Data:

hours = np.array([1,2,3,4,5,6,7,8])
sleep = np.array([5,6,6,7,7,8,8,9])
practice = np.array([10,20,30,40,50,60,70,80])

marks = np.array([35,45,55,65,72,78,85,92])

X = np.column_stack((hours, sleep, practice))

# Model
model = LinearRegression()
model.fit(X, marks)

# Predict button

prediction = model.predict([[5, 7, 50]])



st.markdown(f"""
<div style="
    background: rgba(255,255,255,0.1);
    padding:20px;
    border-radius:15px;
    text-align:center;
">
    <h2>🎯 Predicted Marks: {int(prediction[0])}</h2>
</div>
""", unsafe_allow_html=True)

new_hours = st.number_input("Enter hours studied:", min_value=0.0, max_value=10.0, step=0.5)

new_sleep = st.number_input("Enter hours of sleep:", min_value=0.0, max_value=12.0, step=0.5)

new_practice = st.number_input("Enter number of practice questions:", min_value=0, max_value=100, step=5)   


if st.button("Predict"):
    prediction = model.predict([[new_hours, new_sleep, new_practice]])

    st.markdown(
        f"<h2 style='text-align:center;'>🎯 {int(prediction[0])} Marks</h2>",
        unsafe_allow_html=True
    )
   
    st.metric("Predicted Score", int(prediction[0]))
    st.progress(int(prediction[0]) / 100)



col1, col2, col3 = st.columns(3)

with col1:
    new_hours = st.slider("📚 Study Hours", 0, 10, 1)

with col2:
    new_sleep = st.slider("😴 Sleep Hours", 0, 12, 6)

with col3:
    new_practice = st.slider("📝 Practice Questions", 0, 100, 10)

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Data points
ax.scatter(hours, sleep, marks, c = marks )

# Highlight user input
predicted_value = model.predict([[new_hours, new_sleep, new_practice]])

ax.scatter(new_hours, new_sleep, predicted_value, s=200, c= 'red' )

# Labels
import plotly.express as px

# Create data
fig = px.scatter_3d(
    x=hours,
    y=sleep,
    z=marks,
    color=marks,
    title="📊 Interactive 3D Study Analysis"
)

# Add user prediction point

prediction = model.predict([[new_hours, new_sleep, new_practice]])

fig.add_scatter3d(
    x=[new_hours],
    y=[new_sleep],
    z=[prediction[0]],
    mode='markers',
    marker=dict(size=8, color='red'),
    name="Your Prediction"
)

# Show in Streamlit
st.plotly_chart(fig)
if predicted_value[0] >= 85:
    st.success("🔥 Excellent performance!")
elif predicted_value[0] >= 60:
    st.info("👍 Good, keep improving!")
else:
    st.warning("📉 Need more effort!")


with st.spinner("Analyzing your performance..."):
    prediction = model.predict([[new_hours, new_sleep, new_practice]])

st.session_state.history.append(int(prediction[0]))

data = pd.read_csv("data.csv")

X = data[["hours", "sleep", "practice"]]
y = data["marks"]

model.fit(X, y)

st.write("📜 Prediction History:")
st.write(st.session_state.history)