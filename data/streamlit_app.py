import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Membaca data dari file CSV
data = pd.read_csv('hour.csv')

# Konversi kolom 'dteday' ke format datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Mendefinisikan fungsi untuk menampilkan histogram jam penyewaan
def hourly_rental_distribution():
  plt.figure(figsize=(12, 6))
  sns.histplot(data['hr'], bins=24, kde=False)
  plt.title('Distribusi Penyewaan Sepeda Listrik Pecatu Berdasarkan Jam')
  plt.xlabel('Jam dalam Sehari')
  plt.ylabel('Frekuensi')
  st.pyplot(plt)

# Judul dan deskripsi dashboard
st.title('Analisis Penyewaan Sepeda Listrik Pecatu')
st.write('Dashboard ini menampilkan distribusi jam penyewaan sepeda listrik Pecatu berdasarkan data yang tersedia.')

# Menjalankan fungsi untuk menampilkan histogram
hourly_rental_distribution()

def seasonal_analysis():
  # Group data by month and calculate the mean number of rentals
  monthly_rentals = data.groupby('mnth')['cnt'].mean()

  plt.figure(figsize=(12, 6))
  sns.lineplot(x=monthly_rentals.index, y=monthly_rentals)
  plt.title('Rata-rata Penyewaan Sepeda Listrik per Bulan')
  plt.xlabel('Bulan')
  plt.ylabel('Jumlah Penyewaan')
  st.pyplot(plt)

# Memanggil fungsi untuk menampilkan analisis musiman
seasonal_analysis()

def correlation_heatmap():
  # Menghitung matriks korelasi
  corr_matrix = data.corr()

  plt.figure(figsize=(10, 8))
  sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
  plt.title('Korelasi Antar Fitur')
  st.pyplot(plt)

# Memanggil fungsi untuk menampilkan heatmap
correlation_heatmap()

# Slider untuk memilih tahun
year_slider = st.slider('Pilih Tahun', int(data['yr'].min()), int(data['yr'].max()))
filtered_data = data[data['yr'] == year_slider]
