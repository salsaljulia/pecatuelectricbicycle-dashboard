import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('pecatu_electric_bicycle_data.csv')   


# Create sidebar with filters
st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Start Date", data['tanggal'].min())
end_date = st.sidebar.date_input("End Date", data['tanggal'].max())
selected_station = st.sidebar.selectbox("Station", data['stasiun'].unique())

# Filter data based on user input
filtered_data = data[(data['tanggal'] >= start_date) & (data['tanggal'] <= end_date) & (data['stasiun'] == selected_station)]

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
sns.lineplot(x='jam', y='durasi_sewa', data=filtered_data, err_style='band', ax=ax)
plt.xlabel('Jam')
plt.ylabel('Durasi Sewa Rata-Rata (menit)')
st.pyplot(fig)
