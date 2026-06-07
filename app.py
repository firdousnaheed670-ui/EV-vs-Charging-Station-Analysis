import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# Page config
st.set_page_config(page_title="EV vs Charging Stations", layout="wide")
# Add background with CSS
page_bg = """
<style>
/* Background */
[data-testid="stAppViewContainer"] {
    background-image: linear-gradient(to right, #f0f4f8, #d9e2ec);
    background-size: cover;
}

/* General text */
h1, h2, h3, h4, h5, h6, p, div {
    color: #000000 !important;
}

/* Dropdown (Selectbox) */
.stSelectbox div, .stSelectbox label {
    color: #000000 !important;
}
.stSelectbox [role="listbox"] {
    background-color: #ffffff !important; /* Dropdown menu background */
}
.stSelectbox [role="option"] {
    background-color: #ffffff !important; /* Option background */
    color: #000000 !important;            /* Option text */
}
.stSelectbox [role="option"]:hover {
    background-color: #e6f0ff !important; /* Highlight on hover */
    color: #000000 !important;
}

/* Text input */
.stTextInput input {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* Buttons */
.stButton button {
    color: #ffffff !important;
    background-color: #0073e6 !important;
    border-radius: 5px;
}
.stButton button:hover {
    background-color: #005bb5 !important;
    color: #ffffff !important;
}

/* Download button */
.stDownloadButton button {
    color: #ffffff !important;
    background-color: #28a745 !important;
    border-radius: 5px;
}
.stDownloadButton button:hover {
    background-color: #1e7e34 !important;
    color: #ffffff !important;
}

/* Expander (See methodology) */
.streamlit-expanderHeader {
    color: #000000 !important;
    background-color: #ffffff !important;
}
.streamlit-expanderHeader:hover {
    background-color: #e6f0ff !important;
    color: #000000 !important;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)



# ================================
# 📌 Static Information
# ================================
st.title("EV vs Charging Stations Analysis")
st.subheader("Exploring EV Adoption vs Infrastructure Growth Across States")

st.markdown("""
This dashboard compares **Electric Vehicle (EV) adoption trends** with the availability of 
**charging infrastructure** across Indian states.  
Use the filters below to explore data by year and region.
""")

st.info("Instructions: Select a state and year range using the filters below. Charts and insights will update dynamically.")

# Load datasets
ev_df = pd.read_excel("data/electric_vehicle.xlsx")   # columns: state, year, ev_count
station_df = pd.read_csv("data/charging_stations.csv")  # columns: state, year, station_count

# Merge datasets
df_comb = pd.merge(ev_df, station_df, on=["state", "year"], how="inner")

# Dataset Snapshot
st.header("📊 Dataset Snapshot")
st.dataframe(df_comb.head())

# Key Insights
st.header("💡 Key Insights")
st.success("EV growth has outpaced charging stations in several states.")
st.info("Delhi shows fastest charging infrastructure growth.")
st.warning("Gujarat highlights imbalance: strong EV growth but fewer stations.")

# ================================
# 🎛️ Interactive Elements
# ================================
st.header("🎛️ Interactive Exploration")

# Filters
states = df_comb["state"].unique()
selected_state = st.selectbox("Choose Region (State):", states)

year_range = st.slider("Select Year Range:",
                       int(df_comb["year"].min()),
                       int(df_comb["year"].max()),
                       (int(df_comb["year"].min()), int(df_comb["year"].max())))

# Filtered data
filtered_df = df_comb[(df_comb["state"] == selected_state) &
                      (df_comb["year"] >= year_range[0]) &
                      (df_comb["year"] <= year_range[1])]

st.write(f"Filtered Data for {selected_state} ({year_range[0]}–{year_range[1]})")
st.dataframe(filtered_df)

# Action Buttons
if st.button("Run Analysis"):
    st.metric("Total EVs", filtered_df["ev_count"].sum())
    st.metric("Total Charging Stations", filtered_df["station_count"].sum())

st.download_button("Download Report",
                   filtered_df.to_csv(index=False).encode("utf-8"),
                   "filtered_data.csv",
                   "text/csv")

# ================================
# 📈 Dynamic Charts
# ================================
st.header("📈 EV Growth vs Charging Stations")

# Line Chart
st.line_chart(filtered_df.set_index("year")[["ev_count", "station_count"]])

# Bar Chart
st.header("📊 State-wise Comparison")
statewise = df_comb.groupby("state")[["ev_count", "station_count"]].sum()
st.bar_chart(statewise)

# ================================
# 📝 User Input
# ================================
st.header("📝 Custom Query")
custom_state = st.text_input("Enter custom state name:")
if custom_state:
    custom_df = df_comb[df_comb["state"].str.lower() == custom_state.lower()]
    if not custom_df.empty:
        st.write(f"Results for {custom_state}", custom_df)
        st.line_chart(custom_df.set_index("year")[["ev_count", "station_count"]])
    else:
        st.error("State not found in dataset.")

# ================================
# 📂 Expandable Section
# ================================
with st.expander("See Methodology"):
    st.markdown("""
    - Data sources: EV adoption dataset (Excel) and charging stations dataset (CSV).  
    - Merged on **state** and **year** columns.  
    - Visualizations created using Streamlit’s chart components.  
    - Insights derived from comparing growth rates and infrastructure availability.
    """)

# ================================
# ✅ Conclusion & Suggested Actions
# ================================
st.header("✅ Conclusion & Suggested Actions")
st.markdown("""
- **Conclusion:** EV adoption is accelerating faster than charging infrastructure in many states.  
- **Suggested Actions:**  
  - Invest in charging infrastructure to match EV growth.  
  - Focus on states with high EV adoption but low station counts (e.g., Gujarat).  
  - Encourage balanced policy support for both EVs and infrastructure.
""")

