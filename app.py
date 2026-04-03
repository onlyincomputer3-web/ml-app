import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression

# Title
st.title("📚 Smart Marks Predictor")

st.write("Enter how many hours you studied and get your predicted marks!")

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
    st.success(f"🎯 Predicted Marks: {int(prediction[0])}")

import matplotlib.pyplot as plt

# Plot graph
fig, ax = plt.subplots()
ax.scatter(hours, marks)
ax.plot(hours, model.predict(hours))

ax.set_xlabel("Hours Studied")
ax.set_ylabel("Marks")
ax.set_title("Study Hours vs Marks")

st.pyplot(fig)