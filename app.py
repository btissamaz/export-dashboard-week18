import streamlit as st
import pandas as pd
import plotly.express as px

# Load your Excel file
excel_file = "export_plan_week18.xlsx"
sheet_name = 0

# Read the data
raw_df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)

# Extract shipping info
destination = raw_df.iloc[2, 1]
project = raw_df.iloc[2, 2]
reference = raw_df.iloc[2, 3]
ship_dates = raw_df.iloc[2, 5:]
transport_flags = raw_df.iloc[3, 5:]
eta_dates = raw_df.iloc[4, 5:]

# Build structured data
data = []
for day in ship_dates.index:
    if str(transport_flags[day]).strip().upper() == 'X':
        data.append({
            "Destination": destination,
            "Project": project,
            "Reference": reference,
            "Shipping Date": pd.to_datetime(ship_dates[day]),
            "ETA": pd.to_datetime(eta_dates[day]),
            "Transport Mode": "Truck"  # You can customize this
        })

df = pd.DataFrame(data)

# Streamlit config
st.set_page_config(page_title="Export Expeditions - Week 18", layout="wide")
st.title("🚚 Export Expeditions Dashboard - Week 18")

# Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f0f8ff;
        }
        .css-1d391kg { color: #003366; }
    </style>
""", unsafe_allow_html=True)

# Sidebar filters
if not df.empty and "Project" in df.columns and "Destination" in df.columns:
    project_filter = st.sidebar.multiselect("Select Project", df["Project"].unique(), default=df["Project"].unique())
    destination_filter = st.sidebar.multiselect("Select Destination", df["Destination"].unique(), default=df["Destination"].unique())

    # Filtered data
    filtered_df = df[
        (df["Project"].isin(project_filter)) &
        (df["Destination"].isin(destination_filter))
    ]
else:
    st.warning("⚠️ Your data is missing required columns like 'Project' or 'Destination'. Please check your Excel file.")
    filtered_df = df


else:
    st.warning("⚠️ No expedition data found. Please check your Excel file format.")
    filtered_df = pd.DataFrame()


# Filtered data
filtered_df = df[
    (df["Project"].isin(project_filter)) &
    (df["Destination"].isin(destination_filter))
]

# Timeline chart
fig = px.timeline(
    filtered_df,
    x_start="Shipping Date",
    x_end="ETA",
    y="Reference",
    color="Destination",
    title="Expedition Timeline",
    color_discrete_sequence=["#1f77b4"]
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, use_container_width=True)

# Table
st.subheader("📋 Expedition Details")
st.dataframe(filtered_df.sort_values(by="Shipping Date"))
