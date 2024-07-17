import streamlit as st
import pandas as pd

# Title of the app
st.title('CSV File Loader')

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Input widget to specify the number of rows to display
    num_rows = st.text_input("Enter the number of rows to display:", "10")

    # Selectbox to choose the column to sort by
    sort_column = st.selectbox("Select column to sort by:", df.columns)

    # Buttons to sort the DataFrame
    sort_asc = st.button("Sort Ascending")
    sort_desc = st.button("Sort Descending")

    # Sorting logic
    if sort_asc:
        df = df.sort_values(by=sort_column, ascending=True)
    elif sort_desc:
        df = df.sort_values(by=sort_column, ascending=False)

    try:
        num_rows = int(num_rows)
        if num_rows > len(df):
            num_rows = len(df)
        # Display the specified number of rows of the DataFrame
        st.write(f"Displaying the first {num_rows} rows of the CSV file:")
        st.dataframe(df.head(num_rows))
    except ValueError:
        st.write("Please enter a valid number.")
else:
    st.write("Please upload a CSV file to see its contents.")
