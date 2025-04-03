"""
Frontend logic
"""
import os
from dotenv import load_dotenv
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import st_folium

load_dotenv()

# FastAPI Endpoint URL (Replace with actual API URL)
# if local dev -> 0.0.0.0:8000
endpoint = os.getenv("GCLOUD_RUN_URL") or "http://0.0.0.0:8000"
print(f"Using endpoint: {endpoint}")
URL = f"{endpoint}/predict"

# Streamlit App Title
st.title("🌡 Temperature Prediction")

# Sidebar controls for user input
st.sidebar.header("🦶 Select Step")

# Define the known last date of data (31/12/2023)
last_date = datetime(2023, 12, 31)

# Define the earliest valid date (1st January 2024)
earliest_valid_date = datetime(2024, 1, 1)

# Define the latest valid date (7th January 2024)
latest_valid_date = datetime(2024, 1, 7)

# Date selection (limit between 1st Jan 2024 and 7th Jan 2024)
selected_date = st.sidebar.date_input(
    "Select a date",
    min_value=earliest_valid_date.date(),  # Limit to Jan 1, 2024
    max_value=latest_valid_date.date(),    # Limit to Jan 7, 2024
    value=earliest_valid_date.date()       # Default to the first date
)

# Calculate the difference in days between the selected date and the last known date (31/12/2023)
days_difference = (selected_date - last_date.date()).days

# Display the selected date and the difference
st.sidebar.write(f"Selected date: {selected_date}")
st.sidebar.write(f"Days from 31/12/2023: {days_difference} days")

# Format parameters to match dataset
# Keep this commented out for now
# params = {"date": selected_date.strftime("%Y%m%d")}  # Convert date to YYYYMMDD format

# Use the calculated days difference as the 'steps' parameter
params = {"steps": days_difference}

# Create a placeholder for the prediction result using st.empty() to ensure
# the prediction result is displayed correctly without being overwritten by the map.
# This allows us to dynamically update the prediction in place while keeping the map
prediction_placeholder = st.empty()

# Add the temperature image (daily temperature graph)
st.subheader("📈 Daily Temperature Chart")
image_path = os.path.join(os.path.dirname(__file__), 'images', 'image-Tem-Paris-20250403-min.png')
st.image(image_path, caption="Daily Temperature in Aix-en-Provence")
# The image is for Paris, just for presentation purpose we show "Aix-en-Provence" in the caption

# Button to trigger prediction
if st.sidebar.button("🔍 Predict Temperature"):
    with st.spinner("Fetching temperature prediction..."):
        try:
            response = requests.get(URL, params=params, timeout=3000)
            response.raise_for_status()  # Ensures an exception is raised for HTTP errors (4xx, 5xx)
            response_json = response.json()
            print(response_json)
            predicted_temp = response_json.get("prediction", "N/A")

            # When the prediction is fetched, we update the placeholder with the prediction result.
            # Using the placeholder prevents layout issues and ensures the result stays visible
            # even when other components (like the map) are rendered afterward.
            prediction_placeholder.success(f"🌡 **Predicted Temperature for {selected_date}: {round(predicted_temp, 2)}°C**")

        except requests.exceptions.RequestException as e:
            prediction_placeholder.error(f"❌ Failed to fetch prediction. Error: {e}")

# Map of France with a Pin on Aix-en-Provence
st.subheader("📍 Location: Aix-en-Provence")

# Coordinates for Aix-en-Provence
latitude = 43.529742
longitude = 5.447427

# Create a Folium map centered on France
france_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)  # Coordinates for the center of France

# Add a marker for Aix-en-Provence
folium.Marker([latitude, longitude], popup="Aix-en-Provence").add_to(france_map)

# Display the map in Streamlit using the st_folium function
st_folium(france_map, width=700, height=500)
