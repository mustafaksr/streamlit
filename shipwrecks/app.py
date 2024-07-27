import streamlit as st
import pymongo
import folium
from folium import IFrame
from folium.plugins import MeasureControl, Draw
from io import BytesIO
import pandas as pd
from dotenv import load_dotenv
import os
from streamlit.components.v1 import html

load_dotenv()
DATABASE_PASS = os.environ["DATABASE_PASS"]

# MongoDB connection settings
MONGO_URI = f'mongodb+srv://myAtlasDBUser:{DATABASE_PASS}@edu.xflg0n2.mongodb.net/?retryWrites=true&w=majority&appName=EDU'

DATABASE_NAME = 'sample_geospatial'
COLLECTION_NAME = 'shipwrecks'

def get_shipwrecks(limit=50, bbox=None):
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Build query
    query = {}
    if bbox:
        query = {
            'latdec': {'$gte': bbox['min_lat'], '$lte': bbox['max_lat']},
            'londec': {'$gte': bbox['min_lon'], '$lte': bbox['max_lon']}
        }
    
    # Fetch records with limit and filter
    records = collection.find(query).limit(limit)
    
    # Convert records to a DataFrame
    df = pd.DataFrame(list(records))
    client.close()
    return df

def render_folium_map(df, min_lat, max_lat, min_lon, max_lon):
    # Create a Folium map centered around the initial coordinates
    if df.empty:
        return "<p>No data available</p>"
    
    center_lat = df['latdec'].mean() if not df.empty else (min_lat + max_lat) / 2
    center_lon = df['londec'].mean() if not df.empty else (min_lon + max_lon) / 2
    
    map_ = folium.Map(location=[center_lat, center_lon], zoom_start=2)
    
    # Add shipwreck markers
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latdec'], row['londec']],
            popup=folium.Popup(
                f"Chart: {row['chart']}<br>"
                f"Depth: {row['depth']}<br>"
                f"Watlev: {row['watlev']}",
                max_width=300
            )
        ).add_to(map_)
    
    # Add Drawing and MeasureControl plugins
    draw = Draw()
    draw.add_to(map_)
    
    measure_control = MeasureControl(primary_length_unit='kilometers', secondary_length_unit='miles', primary_area_unit='hectares', secondary_area_unit='acres')
    map_.add_child(measure_control)
    
    # Draw the bounding box based on user inputs
    folium.Rectangle(
        bounds=[[min_lat, min_lon], [max_lat, max_lon]],
        color='blue',
        fill=True,
        fill_opacity=0.1
    ).add_to(map_)

    # Save map to a BytesIO buffer
    map_html = map_._repr_html_()
    return map_html

def main():
    st.title('Shipwreck Locations and Information')
    
    # User input for number of shipwrecks
    total_shipwrecks = st.slider("Select number of shipwrecks to display", min_value=1, max_value=500, value=50)
    
    # User input for geographic bounding box
    st.sidebar.header("Filter by Area")

    min_lat = st.sidebar.slider("Min Latitude", value=-90.0, min_value=-90., max_value=90., format="%.6f")
    max_lat = st.sidebar.slider("Max Latitude", value=90.0, min_value=-90., max_value=90., format="%.6f")
    min_lon = st.sidebar.slider("Min Longitude", value=-180.0, min_value=-180., max_value=180., format="%.6f")
    max_lon = st.sidebar.slider("Max Longitude", value=180.0, min_value=-180., max_value=180., format="%.6f")
    
    # Validate bounding box
    if max_lat <= min_lat:
        st.warning("Max Latitude must be greater than Min Latitude.")
        return
    if max_lon <= min_lon:
        st.warning("Max Longitude must be greater than Min Longitude.")
        return
    
    bbox = {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lon': min_lon,
        'max_lon': max_lon
    }
    
    # Get shipwreck data
    df = get_shipwrecks(limit=total_shipwrecks, bbox=bbox)

    try:
        watlev = st.multiselect("Watlev", df["watlev"].unique(), default="always under water/submerged")
        
        feature_type = st.multiselect("Feature Type", df["feature_type"].unique(), default="Wrecks - Submerged, dangerous")

        df = df[(df["watlev"].isin(watlev)) | (df["feature_type"].isin(feature_type))]

        
    except:
        pass

    # Display the map
    map_html = render_folium_map(df, min_lat, max_lat, min_lon, max_lon)
    st.components.v1.html(map_html, height=600, width=800)

    # Show raw data
    st.write("Shipwreck Data:")
    st.dataframe(df)
    st.write(f"Total Shipwrecks in data: {len(df)}")

if __name__ == "__main__":
    main()
