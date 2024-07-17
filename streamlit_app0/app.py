import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import components
import numpy as np
import matplotlib.pyplot as plt
import math

# Title of the app
st.title('CSV File Loader')

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    bool_cols = [x for x in df.columns if df[x].dtype==bool]
    df[bool_cols] = df[bool_cols].astype(int)

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

    # Scatter plot section
    st.write("## Scatter Plot")
    
    # Select fields for the scatter plot
    x_axis = st.selectbox("Select X-axis field:", df.columns)
    y_axis = st.selectbox("Select Y-axis field:", df.columns)
    
    # Select fields for tooltips
    tooltip_fields = st.multiselect("Select fields for tooltips:", df.columns)

    if x_axis and y_axis:
        # Prepare data for Bokeh plot
        source = ColumnDataSource(df)
        
        # Create a scatter plot with Bokeh
        p = figure(title=f"Scatter Plot: {x_axis} vs {y_axis}", 
                   x_axis_label=x_axis, y_axis_label=y_axis, 
                   tools="pan,wheel_zoom,box_zoom,reset")
        
        # Add scatter plot
        p.circle(x=x_axis, y=y_axis, source=source, size=10, color="navy", alpha=0.5)
        
        # Add tooltips
        tooltips = [(field, f"@{field}") for field in tooltip_fields]
        hover = HoverTool(tooltips=tooltips)
        p.add_tools(hover)
        
        # Display the plot in Streamlit
        script, div = components(p)
        st.bokeh_chart(p)
        
        # Category count plot section
        st.write("## Category Count Plot")
        
        # Filter categorical columns
        cat_cols = [col for col in df.columns if df[col].dtype == 'object']
        
        # Select a categorical field for category counting
        count_field = st.selectbox("Select a categorical field for category count:", cat_cols)
        
        if count_field:
            # Count occurrences of each category
            category_counts = df[count_field].value_counts()
            
            # Create Bokeh bar plot for category counts
            cat_source = ColumnDataSource(data=dict(categories=category_counts.index.tolist(),
                                                    counts=category_counts.tolist()))
            
            p_cat = figure(x_range=category_counts.index.tolist(), plot_height=350,
                           title=f"Category Count for {count_field}", toolbar_location=None, tools="")
            
            p_cat.vbar(x='categories', top='counts', width=0.9, source=cat_source,
                       line_color='white', fill_color='navy', alpha=0.5)
            
            p_cat.xgrid.grid_line_color = None
            p_cat.y_range.start = 0
            
            p_cat.xaxis.major_label_orientation = 1.2
            p_cat.xaxis.axis_label = count_field
            p_cat.yaxis.axis_label = 'Counts'
            
            # Display the category count plot in Streamlit
            st.bokeh_chart(p_cat)
            
            # Column distributions section
            st.write("## Column Distributions")
            
            # Plot all columns as subplots
            fig, axs = plt.subplots(nrows=math.ceil((len(df.columns))**0.5), ncols=math.ceil((len(df.columns))**0.5, ),
                                    figsize=(16, 15))  # Adjust the figsize as needed
            axs = axs.flatten()
            
            for i, col in enumerate(df.columns):
                axs[i].hist(df[col],bins=100)
                axs[i].set_title(col)
                axs[i].set_xlabel('Index')
                axs[i].set_ylabel('Value')
            
            # Hide any unused subplots
            for j in range(i + 1, len(axs)):
                axs[j].axis('off')
            plt.tight_layout()  # Apply tight layout to avoid overlap
            st.pyplot(fig)  # Display the Matplotlib figure containing subplots using Streamlit

else:
    st.write("Please upload a CSV file to see its contents.")
