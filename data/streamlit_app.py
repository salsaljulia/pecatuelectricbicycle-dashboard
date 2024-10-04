import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set title of the app
st.title("Pecatu Electric Bicycle Rental Dashboard")

# Load datasets
hourly_data = pd.read_csv('hour.csv')  # Pastikan file hour.csv berada di direktori yang sama
daily_data = pd.read_csv('day.csv')    # Pastikan file day.csv berada di direktori yang sama

# Convert 'dteday' to datetime
hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

# Display data
if st.checkbox("Show Hourly Data"):
    st.write(hourly_data.head())

if st.checkbox("Show Daily Data"):
    st.write(daily_data.head())

# Distribution of bike rentals by hour
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Jam')
hourly_fig = plt.figure(figsize=(12, 6))
sns.histplot(hourly_data['hr'], bins=24, kde=False)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Jam')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Frekuensi')
st.pyplot(hourly_fig)

# Distribution of bike rentals by season
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Musim')
season_fig = plt.figure(figsize=(12, 6))
sns.countplot(x='season', data=hourly_data)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Frekuensi')
st.pyplot(season_fig)

# Correlation heatmap
st.subheader('Heatmap Korelasi')
numeric_data = hourly_data.select_dtypes(include=[np.number])
correlation_matrix = numeric_data.corr()
heatmap_fig = plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap Korelasi Penyewaan Sepeda')
st.pyplot(heatmap_fig)

# Model Training
st.subheader('Prediksi Penyewaan Sepeda')
fitur = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
target = 'cnt'

X = hourly_data[fitur]
y = hourly_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display model evaluation
st.write("Mean Squared Error (MSE):", mse)
st.write("R-squared Score (R2):", r2)
