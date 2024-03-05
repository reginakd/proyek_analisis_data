import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_sharing(df):
    sumshare_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    sumshare_df = sumshare_df.reset_index()
    return sumshare_df

def create_monthly_sharing(df):
    monthlyshare_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthlyshare_df.index = monthlyshare_df.index.strftime('%B %Y')
    monthlyshare_df.reset_index(inplace=True)  
    return monthlyshare_df

def create_workingday(df):
    workday_df = df.groupby(by="workingday").agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return workday_df

def create_holiday(df):
    holiday_df = df.groupby(by="holiday").agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return holiday_df

def create_hum(df):
    hum_df = df.groupby(by="holiday").agg({
        "dteday": "first",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return hum_df

clean_df = pd.read_csv("main_data.csv")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

with st.sidebar:
    st.subheader("Filter data")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

sumsharing_df = create_sum_sharing(main_df)
monthlysum_df = create_monthly_sharing(main_df)
byday_df = create_workingday(main_df)
byholiday_df = create_holiday(main_df)
byhum_df = create_hum(main_df)

st.header("Bike Sharing :sparkles:")

# menampilkan grafik penyewaan sepeda berdasarkan working day dan holiday setiap bulan
st.subheader("Bike Sharing based on Working Day and Holiday")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(monthlysum_df))
width = 0.35
ax.bar(x - width/2, monthlysum_df['cnt'], width, label='holiday', color='green')
ax.bar(x + width/2, monthlysum_df['casual'] + monthlysum_df['registered'], width, label='working day', color='brown')
ax.set_xticks(x)
ax.set_xticklabels(monthlysum_df['dteday'], rotation=45, ha='right')
ax.legend()
plt.tight_layout()
st.pyplot(fig)

#menampilkan grafik penyewaan sepeda berdasarkan hum setiap bulan
st.subheader("Bike Sharing based on Humidity")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(monthlysum_df))
ax.plot(x, monthlysum_df['cnt'], marker='o', label='hum', color='green')
ax.set_xticks(x)
ax.set_xticklabels(monthlysum_df['dteday'], rotation=45, ha='right')
ax.legend(["hum"])
plt.tight_layout()
st.pyplot(fig)

# Tampilan grafik berdasarkan hari
st.subheader("Performance based on day")
fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(2)
width = 0.40
ax.bar(x-width/2, byday_df['casual'], width, color='green')
ax.bar(x+width/2, byday_df['registered'], width, color='purple')
ax.set_xticks(x+0, (["Holiday", "Weekday"]))
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Tampilan grafik perbulan
st.subheader("Monthly bike shared")
fig, ax = plt.subplots(figsize=(16, 8))
x = monthlysum_df['dteday']
ax.plot(x, monthlysum_df['casual'], marker='o', color='green')
ax.plot(x, monthlysum_df['registered'], marker='o', color='purple')
ax.tick_params(axis='x', rotation=45)
ax.legend(["Casual", "Registered"])
st.pyplot(fig)