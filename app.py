import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("EV Growth vs Charging Stations in India")

# Load datasets
ev_df = pd.read_excel("data/electric_vehicle.xlsx")   
station_df = pd.read_csv("data/charging_stations.csv") 

# Merge on common columns (e.g., state + year)
df_comb = pd.merge(ev_df, station_df, on=["state", "year"],how="inner")

# Show preview
st.write("Combined Dataset Preview:", df_comb.head())

# Plot EV growth vs Charging Stations
st.subheader("EV Growth vs Charging Infrastructure")
plt.figure(figsize=(8,5))
plt.plot(df_comb["year"], df_comb["ev_count"], label="EVs")
plt.plot(df_comb["year"], df_comb["station_count"], label="Charging Stations")
plt.xlabel("Year")
plt.ylabel("Count")
plt.legend()
st.pyplot(plt)
# Dropdown to select a state
selected_state = st.selectbox("Choose a State:", df_comb["state"].unique())

# Filter data based on selection
filtered_df = df_comb[df_comb["state"] == selected_state]

st.write(f"Data for {selected_state}", filtered_df)

# Plot for selected state
plt.figure(figsize=(8,5))
plt.plot(filtered_df["year"], filtered_df["ev_count"], label="EVs")
plt.plot(filtered_df["year"], filtered_df["station_count"], label="Charging Stations")
plt.legend()
st.pyplot(plt)


# Key insights
st.markdown("### Insights")
st.markdown("- Maharashtra leads in EV adoption.")
st.markdown("- Delhi shows fastest charging infra growth.")
st.markdown("- Gujarat has imbalance: strong EV growth but fewer stations.")
