import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Menfinisikan fungsi create_monthly_sharing untuk membuat DataFrame
def create_monthly_sharing(df):
    monthlyshare_df = df.resample(rule='M', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthlyshare_df.index = monthlyshare_df.index.strftime('%B %Y')
    monthlyshare_df = monthlyshare_df.reset_index()
    return monthlyshare_df

# Menfinisikan fungsi create_sum_sharing untuk membuat DataFrame 
def create_sum_sharing(df):
    sumshare_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    sumshare_df = sumshare_df.reset_index()
    return sumshare_df

# Menfinisikan fungsi create_weathersit untuk membuat DataFrame 
def create_weathersit(df):
    weathersit_df = df.groupby(by="weathersit").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    return weathersit_df

# Membaca data dari URL dan konversi kolom 'dteday' menjadi tipe data datetime
clean_df = pd.read_csv("https://raw.githubusercontent.com/reginakd/proyek_analisis_data/main/dashboard/main_data.csv")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

# Menentukan tanggal minimum dan maksimum dari kolom 'dteday'
min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

# Membuat input tanggal
with st.sidebar:
    st.subheader("Choose Date")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Pemilihan tanggal mulai dan akhir 
main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

# Membuat DataFrame df sebelumnya untuk DataFrame utama yang telah difilter
sum_df = create_sum_sharing(main_df)
monthlysum_df = create_monthly_sharing(main_df)
byweather_df = create_weathersit(main_df)

# title untuk header 
st.header("Bike Sharing Dataset :sparkles:")

# grafik penyewa sepeda perbulan
st.subheader("Total of Bike Sharing per Month")
fig, ax = plt.subplots(figsize=(16, 8))
x = monthlysum_df['dteday']
ax.plot(x, monthlysum_df['casual'], marker='o', color = 'green')
ax.plot(x, monthlysum_df['registered'], marker='o', color = 'purple')
ax.tick_params(axis='x', rotation=60)
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# grafik penyewa sepeda perhari setiap tahun
st.subheader("Total of Bike Sharing per Year")
col1, col2, col3 = st.columns(3)
with col1:
    sharesum = sum_df.cnt.sum()
    st.metric("Total (Casual + Registered)", value=sharesum)
with col2:
    sharesum = sum_df.casual.sum()
    st.metric("Casual", value=sharesum)
with col3:
    sharesum = sum_df.registered.sum()
    st.metric("Registered", value=sharesum)

fig, ax = plt.subplots(figsize=(16, 8))
x = sum_df['dteday']
ax.plot(x, sum_df['casual'], marker='o', color='brown')
ax.plot(x, sum_df['registered'], marker='o', color ='blue')
ax.legend(["Casual", "Registered"])
st.pyplot(fig)

# grafik performa penyewa sepeda berdasarkan cuaca
st.subheader("Bike Sharing Based on Weather")
fig, ax = plt.subplots(figsize=(7, 5))
x = np.arange(3)
width = 0.50
ax.bar(x-width/2, byweather_df['casual'], width, color='pink')
ax.bar(x+width/2, byweather_df['registered'], width, color='blue')
ax.set_xticks(x+0, (["Berawan", "Mendung","Gerimis"]))
ax.legend(["Casual", "Registered"])
st.pyplot(fig)
