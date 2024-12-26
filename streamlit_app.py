import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="🎬")
st.title("🎬 Movies dataset")


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).
@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_drought_data_part1.csv")
    return df


df = load_data()

# User filters
# Filter by FIPS (location identifier)
fips_codes = st.multiselect(
    "Select FIPS (Location)",
    options=df["fips"].unique(),
    default=df["fips"].unique()[:5]  # Default: first 5 locations
)

# Filter by date range
dates = pd.to_datetime(df["date"])
min_date, max_date = dates.min(), dates.max()
date_range = st.slider("Select Date Range", min_date, max_date, (min_date, max_date))

# Select metric to visualize
metrics = [
    "PRECTOT",  # Precipitation
    "T2M",      # Mean Temperature
    "T2M_MAX",  # Max Temperature
    "T2M_MIN",  # Min Temperature
    "WS10M",    # Wind Speed at 10m
]
selected_metric = st.selectbox("Select Metric to Visualize", options=metrics)

# Filter data based on user inputs
df_filtered = df[
    (df["fips"].isin(fips_codes)) & 
    (pd.to_datetime(df["date"]).between(date_range[0], date_range[1]))
]

# Visualize selected metric over time
st.write(f"### {selected_metric} Over Time")

if df_filtered.empty:
    st.warning("No data available for the selected filters. Try adjusting your selection.")
else:
    # Line chart of the selected metric over time
    chart = (
        alt.Chart(df_filtered)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y(selected_metric, title=selected_metric),
            color="fips:N",  # Different line for each FIPS
        )
        .properties(height=400)
    )
    st.altair_chart(chart, use_container_width=True)

# Display the filtered dataframe
st.write("### Filtered Dataset")
st.dataframe(df_filtered, use_container_width=True)