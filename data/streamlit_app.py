import pandas as pd
import numpy as np
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set title and layout
st.set_page_config(page_title="Pecatu Electric Bicycle Rental Dashboard", layout="wide")

# Load datasets (ensure files are in the same directory)
try:
    hourly_data = pd.read_csv('hour.csv')
    daily_data = pd.read_csv('day.csv')
except FileNotFoundError:
    st.error("Error: Data files 'hour.csv' and 'day.csv' not found. Please ensure they are in the same directory.")
    st.stop()

# Convert 'dteday' to datetime format
hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

# Data exploration section with collapsible sections
st.header("Data Exploration")
with st.expander("Hourly Data"):
    st.write(hourly_data.head())

with st.expander("Daily Data"):
    st.write(daily_data.head())

# Interactive data selection for visualization
data_type = st.selectbox("Choose Data:", ["Hourly", "Daily"])
if data_type == "Hourly":
    data = hourly_data
else:
    data = daily_data

# Distribution of bike rentals by hour/day
st.subheader(f"Distribusi Penyewaan Sepeda Berdasarkan {data_type.lower()}")
hourly_fig = plt.figure(figsize=(12, 6))
if data_type == "Hourly":
    sns.histplot(data['hr'], bins=24, kde=False)
    plt.xlabel('Jam dalam Sehari')
else:
    sns.histplot(data['dteday'].dt.hour, bins=24, kde=False)
    plt.xlabel('Hari dalam Seminggu')
plt.title(f"Distribusi Penyewaan Sepeda Berdasarkan {data_type.lower()}")
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

# Model Training section with better organization and error handling
st.header("Prediksi Penyewaan Sepeda")

# Feature selection (consider adding feature importance or selection techniques)
fitur = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
target = 'cnt'

try:
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

   # Display model evaluation with clear formatting
    st.subheader("Model Evaluation")
    st.write(f"Mean Squared Error (MSE): {mse:.2f}")
    st.write(f"R-squared Score (R2): {r2:.2f}")

# Visualize actual vs. predicted values
    prediction_fig = plt.figure(figsize=(12, 6))
    plt.scatter(y_test, y_pred)
    plt.xlabel("Actual Bike Rentals")
    plt.ylabel("Predicted Bike Rentals")
    plt.title("Actual vs. Predicted Bike Rentals")
    st.pyplot(prediction_fig)
