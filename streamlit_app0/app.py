import streamlit as st
import pandas as pd


# Title of the app
st.title('CSV File Loader')

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame
    st.write("Here's the data from the CSV file:")
    st.dataframe(df)
else:
    st.write("Please upload a CSV file to see its contents.")


