from mpl_toolkits.mplot3d import Axes3D
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
  
st.set_page_config(page_title="AI Marks Predictor", page_icon="🤖", layout="centered")

# Title
st.markdown(
    "<h1 style='text-align: center; color: #4CAF50;'>📚 AI Marks Predictor</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Predict your marks based on study hours 🚀</p>",
    unsafe_allow_html=True
)
# Data
hours = np.array([1,2,3,4,5,6,7,8])
sleep = np.array([5,6,6,7,7,8,8,9])
practice = np.array([10,20,30,40,50,60,70,80])

marks = np.array([35,45,55,65,72,78,85,92])

X = np.column_stack((hours, sleep, practice))

# Model
model = LinearRegression()
model.fit(X, marks)

# Predict button

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
ax.scatter(hours, sleep, marks)

# Highlight user input
predicted_value = model.predict([[new_hours, new_sleep, new_practice]])

ax.scatter(new_hours, new_sleep, predicted_value, s=200)

# Labels
ax.set_xlabel("Study Hours 📚")
ax.set_ylabel("Sleep Hours 😴")
ax.set_zlabel("Marks 🎯")

ax.set_title("3D Study Analysis")

st.pyplot(fig)  
prediction = model.predict([[new_hours, new_sleep, new_practice]])

st.metric(label="Predicted Score", value=f"{int(prediction[0])}")