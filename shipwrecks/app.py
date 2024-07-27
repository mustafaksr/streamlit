import streamlit as st
import pymongo
import folium
from folium import IFrame
from folium.plugins import MeasureControl
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

def render_folium_map(df, initial_coords=(0, 0)):
    # Create a Folium map centered around the initial coordinates
    if df.empty:
        return "<p>No data available</p>"
    
    center_lat = df['latdec'].mean() if not df.empty else initial_coords[0]
    center_lon = df['londec'].mean() if not df.empty else initial_coords[1]
    
    if center_lat and center_lon:
        map_ = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    else: 
        center_lat , center_lon = 15.28, -76.45
        map_ = folium.Map(location=[center_lat, center_lon], zoom_start=3)
    
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

    # Add ClickForMarker to capture click coordinates
    click_js = """
    function onMapClick(e) {
        var lat = e.latlng.lat;
        var lon = e.latlng.lng;
        Shiny.setInputValue("lat", lat);
        Shiny.setInputValue("lon", lon);
    }
    map.on('click', onMapClick);
    """
    map_.get_root().html.add_child(folium.Element('<script>{}</script>'.format(click_js)))

    # Add MeasureControl for measuring distances and areas
    measure_control = MeasureControl(primary_length_unit='kilometers', secondary_length_unit='miles', primary_area_unit='hectares', secondary_area_unit='acres')
    map_.add_child(measure_control)

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

    # Display the map
    map_html = render_folium_map(df)
    st.components.v1.html(map_html, height=600, width=800)

    # Show raw data
    st.write("Shipwreck Data:")
    st.dataframe(df)

    # Interactive map coordinates
    st.write("Click on the map to select coordinates.")
    selected_lat = st.text_input("Latitude", "")
    selected_lon = st.text_input("Longitude", "")
    if selected_lat and selected_lon:
        st.write(f"Selected Latitude: {selected_lat}, Longitude: {selected_lon}")

if __name__ == "__main__":
    main()
