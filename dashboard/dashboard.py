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
        "cnt": "sum",
        "windspeed": "mean"  
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
    monthlyshare_df = monthlyshare_df.reset_index()
    return monthlyshare_df

def create_yearly_sharing(df):
    yearlyshare_df = df.resample(rule='Y', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
        "windspeed": "mean"  
    })
    yearlyshare_df.index = yearlyshare_df.index.strftime('%Y')
    yearlyshare_df.reset_index(inplace=True)  
    return yearlyshare_df

clean_df = pd.read_csv("https://raw.githubusercontent.com/reginakd/proyek_analisis_data/main/dashboard/main_data.csv")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

with st.sidebar:
    st.subheader("Data Visualization")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

sumsharing_df = create_sum_sharing(main_df)
yearlysum_df = create_yearly_sharing(main_df)
monthlysum_df = create_yearly_sharing(main_df)

st.header("## Bike Sharing Data for Month :sparkles:")

# Grafik jumlah penyewaan sepeda dalam setahun (registered + casual)
st.subheader("Total of Bike Sharing per Year")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(yearlysum_df))
ax.plot(x, yearlysum_df['cnt'], marker='o', label='Total', color='pink')
ax.plot(x, yearlysum_df['casual'] + yearlysum_df['registered'], marker='o', label='Casual + Registered', color='blue')
ax.set_xticks(x)
ax.set_xticklabels(yearlysum_df['dteday'], rotation=60, ha='right')
ax.legend(loc='upper center')
ax.set_ylabel('Total Bike Sharing', font='10')
ax.set_xlabel('Year', font='10')
plt.tight_layout()
st.pyplot(fig)

# Grafik penyewaan sepeda setiap bulan
st.subheader("Total of Bike Sharing per Month")
fig, ax = plt.subplots(figsize=(16, 8))
x = monthlysum_df['dteday']
ax.plot(x, monthlysum_df['casual'], marker='o', color='green')
ax.plot(x, monthlysum_df['registered'], marker='o', color='purple')
ax.tick_params(axis='x', rotation=90)
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# Grafik pengaruh kelembapan terhadap jumlah penyewa sepeda
st.subheader("The Effect of Humidity on Bicycle Sharing per Month")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(main_df['hum'], main_df['cnt'], color='brown', alpha=0.5)
ax.set_xlabel('Hum in %', font='10')
ax.set_ylabel('Total Bike Sharing', font='10')
plt.tight_layout()
st.pyplot(fig)
