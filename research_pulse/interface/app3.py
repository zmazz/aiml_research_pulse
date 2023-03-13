import streamlit as st
from streamlit_option_menu import option_menu

st.markdown(
    f"""
    <style>
        /* Center all text in Streamlit page */
        .stApp {{
            text-align: center;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Add some text to the page
st.write("Hello, world!")


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
