import streamlit as st
import pymongo
import folium
from io import BytesIO
import base64
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_PASS=os.environ["DATABASE_PASS"]

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

def render_folium_map(df):
    # Create a map centered around the average coordinates
    if df.empty:
        return "<p>No data available</p>"
    
    center_lat = df['latdec'].mean()
    center_lon = df['londec'].mean()
    map_ = folium.Map(location=[center_lat, center_lon], zoom_start=10)
    
    # Add shipwreck markers
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latdec'], row['londec']],
            popup=folium.Popup(
                f"Coor.: {row['latdec']}, {row['londec']}<br>"
                f"Depth: {row['depth']}<br>"
                f"Watlev: {row['watlev']}",
                max_width=300
            )
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
    min_lat = st.sidebar.number_input("Min Latitude", value=-90.0, format="%.6f")
    max_lat = st.sidebar.number_input("Max Latitude", value=90.0, format="%.6f")
    min_lon = st.sidebar.number_input("Min Longitude", value=-180.0, format="%.6f")
    max_lon = st.sidebar.number_input("Max Longitude", value=180.0, format="%.6f")
    
    bbox = {
        'min_lat': min_lat,
        'max_lat': max_lat,
        'min_lon': min_lon,
        'max_lon': max_lon
    }
    
    # Get shipwreck data
    df = get_shipwrecks(limit=total_shipwrecks, bbox=bbox)
    
    # Render Folium map
    map_html = render_folium_map(df)
    st.components.v1.html(map_html, height=600, width=800)

    # Show raw data
    st.write("Shipwreck Data:")
    st.dataframe(df)

if __name__ == "__main__":
    main()
