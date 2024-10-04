import pandas as pd
import streamlit as st

# Membaca data dari file CSV
hourly_data = pd.read_csv('hour.csv')  # Ganti dengan path yang sesuai jika diperlukan

# Mengubah kolom 'dteday' menjadi format datetime
hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])

# Total penyewaan
total_rentals = hourly_data['cnt'].sum()

# Jam terpopuler untuk penyewaan
popular_hours = hourly_data.groupby('hr')['cnt'].sum().sort_values(ascending=False).reset_index()

# Musim terpopuler untuk penyewaan
popular_seasons = hourly_data.groupby('season')['cnt'].sum().sort_values(ascending=False).reset_index()

# Membuat tampilan aplikasi Streamlit
st.title('Penyewaan Sepeda Listrik di Pecatu Electric Bicycle')

st.header('Total Penyewaan')
st.write(f'Total penyewaan sepeda listrik: **{total_rentals}**')

# Menampilkan jam terpopuler
st.header('Jam Terpopuler untuk Penyewaan')
st.write('Jam dan jumlah penyewaan:')
st.bar_chart(popular_hours.set_index('hr'))

# Menampilkan musim terpopuler
st.header('Musim Terpopuler untuk Penyewaan')
season_names = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
popular_seasons['season_name'] = popular_seasons['season'].map(season_names)
st.write('Musim dan jumlah penyewaan:')
st.bar_chart(popular_seasons.set_index('season_name')['cnt'])

# Menampilkan informasi lebih lanjut
st.sidebar.header('Informasi')
st.sidebar.write('Aplikasi ini memberikan informasi tentang penyewaan sepeda listrik berdasarkan jam dan musim.')
