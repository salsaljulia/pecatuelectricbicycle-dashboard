import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Set visual style
sns.set(style='dark')

# Helper functions to create various dataframes
def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='rental_date').agg({
        "rental_id": "nunique",
        "total_price": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "rental_id": "rental_count",
        "total_price": "revenue"
    }, inplace=True)
    
    return daily_rentals_df

def create_sum_bike_items_df(df):
    sum_bike_items_df = df.groupby("bike_model").quantity.sum().sort_values(ascending=False).reset_index()
    return sum_bike_items_df

def create_by_gender_df(df):
    by_gender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
    by_gender_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return by_gender_df

def create_by_age_df(df):
    by_age_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    by_age_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    by_age_df['age_group'] = pd.Categorical(by_age_df['age_group'], ["Youth", "Adults", "Seniors"])
    
    return by_age_df

def create_by_state_df(df):
    by_state_df = df.groupby(by="state").customer_id.nunique().reset_index()
    by_state_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return by_state_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "rental_date": "max",  # mengambil tanggal rental terakhir
        "rental_id": "nunique",
        "total_price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_rental_timestamp", "frequency", "monetary"]
    
    rfm_df["max_rental_timestamp"] = rfm_df["max_rental_timestamp"].dt.date
    recent_date = df["rental_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_rental_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_rental_timestamp", axis=1, inplace=True)
    
    return rfm_df

# Load cleaned data
all_df = pd.read_csv("bicycle_rentals.csv")  # Pastikan file ini sesuai dengan data penyewaan sepeda listrik

# Convert date columns to datetime
datetime_columns = ["rental_date", "return_date"]
all_df.sort_values(by="rental_date", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["rental_date"].min()
max_date = all_df["rental_date"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["rental_date"] >= str(start_date)) & 
                  (all_df["rental_date"] <= str(end_date))]

# Prepare various dataframes
daily_rentals_df = create_daily_rentals_df(main_df)
sum_bike_items_df = create_sum_bike_items_df(main_df)
by_gender_df = create_by_gender_df(main_df)
by_age_df = create_by_age_df(main_df)
by_state_df = create_by_state_df(main_df)
rfm_df = create_rfm_df(main_df)

# Dashboard Title
st.header('Pecatu Electric Bicycle Rental Dashboard :sparkles:')
st.subheader('Daily Rentals')

col1, col2 = st.columns(2)

with col1:
    total_rentals = daily_rentals_df.rental_count.sum()
    st.metric("Total Rentals", value=total_rentals)

with col2:
    total_revenue = format_currency(daily_rentals_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)

# Plot daily rentals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_rentals_df["rental_date"],
    daily_rentals_df["rental_count"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Product performance
st.subheader("Best & Worst Performing Bike Models")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="quantity", y="bike_model", data=sum_bike_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Rentals", fontsize=30)
ax[0].set_title("Best Performing Bike Models", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="quantity", y="bike_model", data=sum_bike_items_df.sort_values(by="quantity", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Rentals", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Bike Models", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Customer demographics
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    sns.barplot(
        y="customer_count", 
        x="gender",
        data=by_gender_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customers by Gender", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(
        y="customer_count", 
        x="age_group",
        data=by_age_df.sort_values(by="age_group", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customers by Age Group", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Customers by state
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="state",
    data=by_state_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customers by State", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Best Customers based on RFM Parameters
st.subheader("Best Customers Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_monetary)

# Plot RFM metrics
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Customer ID", fontsize=30)
ax[0].set_title("Top Customers by Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Customer ID", fontsize=30)
ax[1].set_title("Top Customers by Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Customer ID", fontsize=30)
ax[2].set_title("Top Customers by Monetary Value", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

# Footer
st.sidebar.header("About")
st.sidebar.text("This dashboard provides insights into the rental patterns of electric bicycles in Pecatu.")
st.sidebar.text("Created by [Your Name]")
