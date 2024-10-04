import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Fungsi untuk memuat data
@st.cache_data  # Meng-cache data untuk meningkatkan performa
def load_data():
    hourly_data = pd.read_csv('hour.csv')  # Ganti dengan path yang sesuai jika diperlukan
    daily_data = pd.read_csv('day.csv')  # Ganti dengan path yang sesuai jika diperlukan
    hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
    daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])
    return hourly_data, daily_data

hourly_data, daily_data = load_data()

# Judul aplikasi
st.title('Analisis Penyewaan Pecatu Electric Bicycle')

# Menampilkan data awal
if st.checkbox('Tampilkan Data Awal'):
    st.subheader('Data Jam')
    st.write(hourly_data.head())
    st.subheader('Data Hari')
    st.write(daily_data.head())

# Distribusi penyewaan berdasarkan jam
st.subheader('Distribusi Penyewaan Berdasarkan Jam')
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(hourly_data['hr'], bins=24, kde=False, ax=ax)
ax.set_title('Distribusi Penyewaan Pecatu Electric Bicycle Berdasarkan Jam')
ax.set_xlabel('Jam dalam Sehari')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Distribusi penyewaan berdasarkan musim
st.subheader('Distribusi Penyewaan Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(12, 6))
sns.countplot(x='season', data=hourly_data, ax=ax)
ax.set_title('Distribusi Penyewaan Pecatu Electric Bicycle Berdasarkan Musim')
ax.set_xlabel('Musim')
ax.set_ylabel('Frekuensi')
st.pyplot(fig)

# Analisis korelasi
st.subheader('Heatmap Korelasi')
numeric_data = hourly_data.select_dtypes(include=[np.number])
correlation_matrix = numeric_data.corr()
fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
ax.set_title('Heatmap Korelasi Pecatu Electric Bicycle')
st.pyplot(fig)

# Model regresi
st.subheader('Model Regresi')
fitur = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
target = 'cnt'

X = hourly_data[fitur]
y = hourly_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluasi model
mse = mean_squared_error(y_test, y_pred)  # Menghitung Mean Squared Error
r2 = r2_score(y_test, y_pred)  # Menghitung R2 Score

st.write(f'Mean Squared Error: **{mse:.2f}**')
st.write(f'R2 Score: **{r2:.2f}**')
