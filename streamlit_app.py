import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    data = pd.read_csv('hour.csv')
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

hourly_data = load_data()

total_rentals = hourly_data['cnt'].sum()

popular_hours = hourly_data.groupby('hr')['cnt'].sum().sort_values(ascending=False).reset_index()

popular_seasons = hourly_data.groupby('season')['cnt'].sum().sort_values(ascending=False).reset_index()

st.title('Penyewaan Sepeda Listrik di Pecatu Electric Bicycle')

st.header('Total Penyewaan')
st.write(f'Total penyewaan sepeda listrik: **{total_rentals}**')

st.header('Jam Terpopuler untuk Penyewaan')
st.bar_chart(popular_hours.set_index('hr'))

st.header('Musim Terpopuler untuk Penyewaan')
season_names = {1: 'Musim Dingin', 2: 'Musim Semi', 3: 'Musim Panas', 4: 'Musim Gugur'}
popular_seasons['season_name'] = popular_seasons['season'].map(season_names)
st.bar_chart(popular_seasons.set_index('season_name')['cnt'])

st.sidebar.header('Informasi')
st.sidebar.write('Aplikasi ini memberikan informasi tentang penyewaan sepeda listrik berdasarkan jam dan musim.')
