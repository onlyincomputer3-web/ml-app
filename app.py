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
hours = np.array([1,2,3,4,5]).reshape(-1,1)
marks = np.array([40,50,60,70,80])

# Model
model = LinearRegression()
model.fit(hours, marks)

# Input slider
new_hours = st.slider("Hours studied", 0, 10, 1)

# Predict button
if st.button("Predict"):
    prediction = model.predict([[new_hours]])

    st.markdown(
        f"<h2 style='text-align:center; color:#FF5733;'>🎯 {int(prediction[0])} Marks</h2>",
        unsafe_allow_html=True
    )
import matplotlib.pyplot as plt

# Plot graph
fig, ax = plt.subplots()
ax.scatter(hours, marks)
ax.plot(hours, model.predict(hours))

ax.set_xlabel("Hours Studied")
ax.set_ylabel("Marks")
ax.set_title("Study Hours vs Marks")

st.pyplot(fig)