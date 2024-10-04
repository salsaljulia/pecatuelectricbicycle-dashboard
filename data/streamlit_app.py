import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('day.csv')
data = pd.read_csv('hour.csv')

# Create sidebar with filters
st.sidebar.title("Filter Data")
start_date = st.sidebar.daily_data("Start Date", data[''].min())
end_date = st.sidebar.date_input("End Date", data['dteday'].max())
selected_station = st.sidebar.selectbox("Station", data['stasiun'].unique())

# Filter data based on user input
filtered_data = data[(data['dteday'] >= start_date) & (data['dteday'] <= end_date) & (data['stasiun'] == selected_station)]

# Create main page with visualizations
st.title("Dashboard Sepeda Listrik Pecatu")

# Visualisasi 1: Jumlah penyewaan per hari
st.subheader("Jumlah Penyewaan Per Hari")
fig, ax = plt.subplots()
sns.countplot(x='tanggal', data=filtered_data, ax=ax)
st.pyplot(fig)

# Visualisasi 2: Durasi penyewaan rata-rata per jam
st.subheader("Durasi Penyewaan Rata-Rata Per Jam")
fig, ax = plt.subplots()
sns.lineplot(x='hour', y='duration', data=filtered_data, err_style='band', ax=ax)
plt.xlabel('Hour')
plt.ylabel('Durasi Sewa Rata-Rata (menit)')
st.pyplot(fig)
