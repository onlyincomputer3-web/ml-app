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


# Predict button

new_hours = st.number_input("Enter hours studied:", min_value=0.0, max_value=10.0, step=0.5)

if st.button("Predict"):
    prediction = model.predict([[new_hours]])

    st.markdown(
        f"<h2 style='text-align:center;'>🎯 {int(prediction[0])} Marks</h2>",
        unsafe_allow_html=True
    )

    st.metric("Predicted Score", int(prediction[0]))
    st.progress(int(prediction[0]) / 100)



col1, col2 = st.columns(2)

with col1:
    new_hours = st.slider("Hours studied", 0, 10, 1, key="hours_slider")

with col2:
    st.write("Adjust your study time 📚")


import matplotlib.pyplot as plt


fig, ax = plt.subplots()

# Scatter (data points)
ax.scatter(hours, marks)

# Prediction line
ax.plot(hours, model.predict(hours))

# Highlight user input
ax.scatter(new_hours, model.predict([[new_hours]]), s=200)

ax.set_xlabel("Hours Studied")
ax.set_ylabel("Marks")
ax.set_title("📊 Study vs Marks")

st.pyplot(fig)
  
prediction = model.predict([[new_hours]])

st.metric(label="Predicted Score", value=f"{int(prediction[0])}")