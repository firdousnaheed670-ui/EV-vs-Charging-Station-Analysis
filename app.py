import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("EV Growth vs Charging Stations in India")

# Load datasets
ev_df = pd.read_csv("file_path")      # replace with actual extension, e.g., file_path.csv
station_df = pd.read_csv("file_path1")  # replace with actual extension, e.g., file_path1.csv

# Merge on common columns (e.g., state + year)
df_comb = pd.merge(ev_df, station_df, on=["State", "Year"])

# Show preview
st.write("Combined Dataset Preview:", df_comb.head())

# Plot EV growth vs Charging Stations
st.subheader("EV Growth vs Charging Infrastructure")
plt.figure(figsize=(8,5))
plt.plot(df_comb["Year"], df_comb["EV_Count"], label="EVs")
plt.plot(df_comb["Year"], df_comb["Station_Count"], label="Charging Stations")
plt.legend()
st.pyplot(plt)

# Key insights
st.markdown("### Insights")
st.markdown("- Maharashtra leads in EV adoption.")
st.markdown("- Delhi shows fastest charging infra growth.")
st.markdown("- Gujarat has imbalance: strong EV growth but fewer stations.")
