import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# memuat dataset
main_data = pd.read_csv("https://raw.githubusercontent.com/reginakd/proyek_analisis_data/main/dashboard/main_data.csv")

def create_hum(df):
    hum_df = df.groupby(by="hum").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()  
    return hum_df

def create_temp(df):
    temp_df = df.groupby(by="temp").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()  
    return temp_df

def create_windspeed(df):
    windspeed_df = df.groupby(by="windspeed").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()  
    return windspeed_df

# memilih opsi bulan
selected_month = st.sidebar.selectbox("Select Month", range(1, 13), 1)

# filter data berdasarkan bulan yang dipilih
filtered_data = main_data[main_data['mnth'] == selected_month]

# judul dataset
st.title("Bike Sharing Data Dashboard")

# menampilkan dataset
st.write("## Bike Sharing Data for Month :sparkles:", selected_month)
st.write(filtered_data)

# Visualisasi data
st.write("## Data Visualizations")

# grafik untuk jumlah rental berdasarkan hari dalam sebulan
plt.figure(figsize=(10, 6))
sns.barplot(data=filtered_data, x='dteday', y='cnt', ci=None)
plt.title("Total Rental Count by Day")
plt.xticks(rotation=90)
fig, ax = plt.subplots()
ax.bar(filtered_data['dteday'], filtered_data['cnt'])
ax.tick_params(axis='x', labelsize=5)  # 
plt.xticks(rotation=90)
st.pyplot(fig)

# grafik untuk suhu dan perasaan suhu berdasarkan hari dalam sebulan
plt.figure(figsize=(10, 6))
sns.boxplot(data=filtered_data, x='dteday', y='temp', color='skyblue', width=0.4, linewidth=1)
sns.boxplot(data=filtered_data, x='dteday', y='atemp', color='orange', width=0.4, linewidth=1)
plt.title("Temperature and Feeling Temperature by Day")
plt.xticks(rotation=45)
plt.legend(labels=['Temperature', 'Feeling Temperature'])
fig, ax = plt.subplots()
ax.boxplot([filtered_data['temp'], filtered_data['atemp']], positions=[1, 2])
ax.set_xticklabels(['Temperature', 'Feeling Temperature'])
plt.xticks(rotation=45)
st.pyplot(fig)

# grafik untuk kelembaban dan kecepatan angin
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered_data, x='hum', y='windspeed', hue='weathersit', palette='viridis', alpha=0.7)
plt.title("Humidity vs Wind Speed")
fig, ax = plt.subplots()
ax.scatter(filtered_data['hum'], filtered_data['windspeed'])
plt.title("Humidity vs Wind Speed")
st.pyplot(fig)

