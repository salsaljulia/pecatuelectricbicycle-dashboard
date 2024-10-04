import pandas as pd
import streamlit as st

hourly_data = pd.read_csv('hour.csv')
daily_data = pd.read_csv('day.csv') 

hourly_data.head()

daily_data.head()

hourly_data['dteday'] = pd.to_datetime(hourly_data['dteday'])
daily_data['dteday'] = pd.to_datetime(daily_data['dteday'])

plt.figure(figsize=(12, 6))
sns.histplot(hourly_data['hr'], bins=24, kde=False)
plt.title('Distribusi Penyewaan Pecatu Electric Bicycle Berdasarkan Jam')
plt.xlabel('Jam dalam Sehari')
plt.ylabel('Frekuensi')
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='season', data=hourly_data)
plt.title('Distribusi Penyewaan Pecatu Electric Bicycle Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Frekuensi')
plt.show()

numeric_data = hourly_data.select_dtypes(include=[np.number])

correlation_matrix = numeric_data.corr()

plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Heatmap Korelasi Pecatu Electric Bicycle')
plt.show()

fitur = ['season', 'yr', 'mnth', 'hr', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed']
target = 'cnt'

X = hourly_data[fitur]
y = hourly_data[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)  # Menghitung Mean Squared Error
r2 = r2_score(y_test, y_pred)  # Menghitung R2 Score
mse, r2
