import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load data
data = pd.read_csv('data.csv')

# Preprocessing data (jika diperlukan)

# Split data menjadi fitur dan target
X = data[['feature1', 'feature2']]  # Ganti dengan fitur yang Anda gunakan
y = data['target']

# Split data menjadi data training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Buat model
model = LinearRegression()
model.fit(X_train, y_train)

# Buat prediksi
y_pred = model.predict(X_test)

# Buat grafik
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
ax.set_xlabel('Actual')
ax.set_ylabel('Predicted')
st.pyplot(fig)

# Tampilkan metrik evaluasi model
st.write('Mean Squared Error:', mean_squared_error(y_test, y_pred))
st.write('R-squared:', r2_score(y_test, y_pred))
