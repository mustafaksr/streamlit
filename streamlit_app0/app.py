import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import components
import numpy as np
import matplotlib.pyplot as plt
import math

# Define the pages as separate functions
def page_home():
    st.title("Home")
    st.write("Welcome to the Home Page!")

def page_test():
    st.title("Test")
    st.write("This is the Test Page.")
    # Insert containers separated into tabs:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Tab 1 EDA", "Tab2 radio","Tab3 Widgets", "Tab4 - SQL conn","Tab 5 - Columns", "Tab 6 - Chat"])
    tab1.write("# this is tab 1")
    tab2.write("# this is tab 2")
    tab3.write("# this is tab 3")
    tab4.write("## this is tab 4")
    tab4.write("## mysql connection")
    tab5.write("# Columns")
    tab6.write("# Chat")

    with tab6:
        # Insert a chat message container.
        with st.chat_message("user"):
            st.write("Hello 👋")
            st.line_chart(np.random.randn(30, 3))
            chart_data = pd.DataFrame(np.random.randn(30,3),columns=["feature_1", "feature_2","size"])
            chart_data['class'] = np.random.choice(['A','B'], 30)
            st.scatter_chart(data=chart_data, x="feature_1",y="feature_2", color="class",size='size')

        # Display a chat input widget.
        st.chat_input("Say something")

    with tab5:
        col1, col2 = st.columns(2)
        col1.write('Column 1')
        col2.write('Column 2')

        # Three columns with different widths
        col1, col2, col3 = st.columns([3,1,1])
        # col1 is wider

        # Using 'with' notation:
        with col1:
            st.write('This is column 1')
            st.text_input('Enter some text',key="cols1text")
            st.number_input('Enter a number',key="cols1number")
            st.text_area('Area for textual entry',key="cols1textarea")
        with col2:
            st.write('This is column 2')
            st.text_input('Enter some text',key="cols2text")
            st.number_input('Enter a number',key="cols2nummber")
            st.text_area('Area for textual entry',key="cols2textarea")
        with col3:
            st.write('This is column 3')
            st.text_input('Enter some text',key="cols3text")
            st.number_input('Enter a number',key="cols3number")
            st.text_area('Area for textual entry',key="cols3textarea")      
    with tab4:
        # Initialize connection.
        conn = st.connection('mysql', type='sql')

        # Perform query.
        df = conn.query('SELECT * from wp_users;', ttl=600)

        # Print results.
        for row in df.itertuples():
            st.write(f"user_login : {row.user_login} |  user_pass : {row.user_pass}:")

        st.write("# df")
        st.dataframe(df)

        st.write("# df columns")
        st.dataframe(df[["user_login","user_pass"]])

        st.write("# user defined columns")
        count_field = st.multiselect("Select a categorical field for category count:", df.columns)
        st.dataframe(df[count_field])

    # You can also use "with" notation:
    with tab2:
        st.radio('Select one:', [1, 2])



    with tab1:
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
            num_rows = st.text_input("Enter the number of rows to display:", "10",key="number")

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
    with tab3:
        if st.button('Say hello'):
            st.write('Why hello there')
        else:
            st.write('Goodbye')

            st.text('Fixed width text')
            st.markdown('_Markdown_') # see #*
            st.caption('Balloons. Hundreds of them...')
            st.latex(r''' e^{i\pi} + 1 = 0 ''')
            st.write('Most objects') # df, err, func, keras!
            st.write(['st', 'is <', 3]) # see *
            st.title('My title')
            st.header('My header')
            st.subheader('My sub')
            st.code('for i in range(8): foo()')

            st.button('Hit me')
            st.checkbox('Check me out')
            st.radio('Pick one:', ['nose','ear'])
            st.selectbox('Select', [1,2,3])
            st.multiselect('Multiselect', [1,2,3])
            st.slider('Slide me', min_value=0, max_value=10)
            st.select_slider('Slide to select', options=[1,'2'])
            st.text_input('Enter some text',key="example")
            st.number_input('Enter a number')
            st.text_area('Area for textual entry')
            st.date_input('Date input')
            st.time_input('Time entry')
            data = st.file_uploader('File uploader')
            if data:
                st.download_button('Download data', data)

            st.camera_input("一二三,茄子!")
            st.color_picker('Pick a color')
            # * optional kwarg unsafe_allow_html = True
    

def page_contact():
    st.title("Contact")
    st.write("This is the Contact Page.")

# Create a sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Test", "Contact"])

# Show the selected page
if page == "Home":
    page_home()
elif page == "Test":
    page_test()
elif page == "Contact":
    page_contact()


