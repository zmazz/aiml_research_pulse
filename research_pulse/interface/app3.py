import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from PIL import Image
#import logic.analytics_general as ag
#from logic.analytics_general import *

# Set up BigQuery credentials
# client = bigquery.Client.from_service_account_json('deepdipper_data/data/processed')

# # Define your SQL query
# query = """
# SELECT *
# FROM arxiv.clearned.merged
# """

# # Execute the query and read the results into a DataFrame
# df = pd.read_gbq(query, project_id='DeepDipper', credentials=client)

# @st.cache
# def load_data():
#     data = pd.read_cs(r"C:\Users\samue\Projects\research_pulse\data_processed_aiml_arxiv_with_cit.csv")
#     return data

# data = load_data()


st.set_page_config(
    page_title="Research Pulse",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.markdown("<h5 style='text-align: center; color: white;'>Research Pulse</h5>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: white;'>NLP toolkits to master your exploration of research paper</h6>", unsafe_allow_html=True)

html_temp = """
            <div style="background-color:{};padding:1px">
            </div>
            """

st.markdown(
    """
    <style>
        button[title^=Exit]+div [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

Dashboard, Search, Research = st.tabs(["Dashboard", "Search","Research"])

with Dashboard:
        col1, col2= st.columns(2)
        with col1 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/1-Numbers-of-Publications-per-Year.png', caption='Numbers of Publications per Year', use_column_width=True)
            # image1 = Image.open('https://storage.googleapis.com/deepdipper_data/images/1-Numbers-of-Publications-per-Year.png')
            # col1.image(image1, caption='Numbers of Publications per Year', width=700)
        with col2 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/2-Number-of-Publications-by-Year-and-Categ.png', caption='Numbers of Publications by year and by category', use_column_width=True)
            # image2 = Image.open('https://storage.googleapis.com/deepdipper_data/images/2-Number-of-Publications-by-Year-and-Categ.png')
            # col2.image(image2, caption='Numbers of Publications by year and by category', width=700)

        col3, col4= st.columns(2)
        with col3 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/3-Citations-vs-Publications.png', caption='Citations vs Publications', use_column_width=True)
        with col4 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/4-Publications-and-Citations-by-Category-and-Year.png', caption='Publications and Citaions by category and year', use_column_width=True)

        col5, col6 = st.columns(2)
        with col5 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/5-Top-cited-authors.png', caption='Top cited authors', use_column_width=True)
        with col6 :
            st.image('https://storage.googleapis.com/deepdipper_data/images/6-Top-cited-authors-by-category.png', caption='Top cited authors by category', use_column_width=True)

        st.image('https://storage.googleapis.com/deepdipper_data/images/7-Treemap.png', caption='Treemap of keywords', use_column_width=True)

        # col8, col9 = st.columns(2)
        # with col8 :
        #     col8.plotly_chart(ag.growth_of_ai_ml_over_years())
        # with col9 :
        #     col9.plotly_chart(ag.papers_published_over_the_month())

        # col10, col11 = st.columns(2)
        # with col10 :
        #     col10.plotly_chart(ag.papers_published_over_the_year())
        # with col11 :
        #     col11.plotly_chart(ag.papers_published_over_the_day())

        # fig = px.scatter(
        #         df.query("clean_merged == 'True'"),
        #         x="num_cit",
        #         y="category",
        #         size="pop",
        #         color="continent",
        #         hover_name="country",
        #         log_x=True,
        #         size_max=60,
        #     )
        #Dashboard.plotly_chart(fig, theme="streamlit", use_container_width=True)

        # Dashboard.write(df)

    #End of Dashboard view

with Search:
    with st.form(key='params_for_api1'):
        query = st.text_input('Input topic or notion to get most relevent papers:')
        st.form_submit_button('Browse the arXiv net!')

    import streamlit as st

    # @st.cache_data(persist="disk")
    # def fetch_and_clean_data(url):
    #     # Fetch data from URL here, and then clean it up.
    #     return data

    # fetch_and_clean_data.clear()
    # d1 = fetch_and_clean_data(DATA_URL)
    # # Actually executes the function, since this is the first time it was
    # # encountered.

    # d2 = fetch_and_clean_data(DATA_URL_1)
    # # Does not execute the function. Instead, returns its previously computed
    # # value. This means that now the data in d1 is the same as in d2.

    # d3 = fetch_and_clean_data(DATA_URL_2)
    # This is a different URL, so the function executes.


with Research:
    with st.form(key='params_for_api2'):
        query = st.text_input('Input topic or notion to get most relevent papers:')
        st.form_submit_button('Browse the arXiv net!')

    # @st.cache_data(persist="disk")
    # def fetch_and_clean_data(url):
    #     # Fetch data from URL here, and then clean it up.
    #     return data

    # fetch_and_clean_data.clear()
    # d1 = fetch_and_clean_data(DATA_URL)
    # # Actually executes the function, since this is the first time it was
    # # encountered.

    # d2 = fetch_and_clean_data(DATA_URL_1)
    # # Does not execute the function. Instead, returns its previously computed
    # # value. This means that now the data in d1 is the same as in d2.

    # d3 = fetch_and_clean_data(DATA_URL_2)
    # This is a different URL, so the function executes.






# import streamlit as st
# from streamlit_option_menu import option_menu

# st.markdown(
#     f"""
#     <style>
#         /* Center all text in Streamlit page */
#         .stApp {{
#             text-align: center;
#         }}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Add some text to the page
# st.write("Hello, world!")


# # Create a container to hold all elements
# container = st.beta_container()

# # Add all elements to the container
# container.header("My Streamlit Page")
# container.write("Welcome to my page!")
# container.button("Click me")

# # Apply CSS to center the container
# container.markdown(
#     f"""
#     <style>
#         .reportview-container .main .block-container {{
#             max-width: 1000px;
#             padding-top: 1rem;
#             padding-right: 1rem;
#             padding-left: 1rem;
#             padding-bottom: 1rem;
#             margin: auto;
#         }}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
# # # Set page layout and configuration
# # st.set_page_config(page_title="My App", page_icon=":smiley:", layout="wide")

# # # Create a container for the top navigation bar
# # top_container = st.container()

# # # Add elements to the top container
# # with top_container:
# #     st.write("My App")
# #     st.write("Home")
# #     st.write("About")
# #     st.write("Contact")

# # # Add other content to the main page
# # st.write("Welcome to my app!")

# # # with st.sidebar:
# # #     choose = option_menu("App Gallery", ["About", "Photo Editing", "Project Planning", "Python e-Course", "Contact"],
# # #                          icons=['house', 'camera fill', 'kanban', 'book','person lines fill'],
# # #                          menu_icon="app-indicator", default_index=0, orientation='horizontal',
# # #                          styles={
# # #         "container": {"padding": "5!important", "background-color": "#fafafa"},
# # #         "icon": {"color": "green", "font-size": "20px"},
# # #         "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
# # #         "nav-link-selected": {"background-color": "#02ab21"},
# # #     }
# # #     )
