import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

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


movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")

import time

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1, text=progress_text)

html_temp = """
            <div style="background-color:{};padding:1px">
            </div>
            """

languages = {
    'English': 'eng',
    'French': 'fra',
}

tab1, tab2, tab3 = st.tabs(["Dashboard", "Search","Research"])

with tab1:
    st.header("Dashboard")
    score_rating = movies_data['score'].unique().tolist()
    genre_list = movies_data['genre'].unique().tolist()
    st.write("""Stats board""")
    year_list = movies_data['year'].unique().tolist()

    avg_budget = movies_data.groupby('genre')['budget'].mean().round()
    avg_budget = avg_budget.reset_index()
    genre = avg_budget['genre']
    avg_bud = avg_budget['budget']
    
    col1, col2, col3 = st.columns([3, 3, 3])

    with col1:
        fig = plt.figure(figsize = (19, 10))
        plt.bar(genre, avg_bud, color = 'blue')
        plt.xlabel('genre')
        plt.ylabel('budget')
        plt.title('Statistics')
        st.pyplot(fig)

    with col2:
        st.pyplot(fig)

    with col3:
        st.pyplot(fig)

    year_col, continent_col, log_x_col = st.columns([5, 5, 5])
    
    with year_col:
        year_choice = st.slider(
            "What year would you like to examine?",
            min_value=1952,
            max_value=2007,
            step=5,
            value=2007,
        )
    with continent_col:
        continent_choice = st.selectbox(
            "What continent would you like to look at?",
            ("All", "Asia", "Europe", "Africa", "Americas", "Oceania"),
        )
    with log_x_col:
        log_x_choice = st.checkbox("Log X Axis?")

    # -- Read in the data
    df = px.data.gapminder()
    # -- Apply the year filter given by the user
    filtered_df = df[(df.year == year_choice)]
    # -- Apply the continent filter
    if continent_choice != "All":
        filtered_df = filtered_df[filtered_df.continent == continent_choice]

    # -- Create the figure in Plotly
    fig = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=log_x_choice,
        size_max=60,
    )
    fig.update_layout(title="GDP per Capita vs. Life Expectancy")
    # -- Input the Plotly chart to the Streamlit interface
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(movies_data)
    st.dataframe(df.style.highlight_max(axis=0))

    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
    st.line_chart(chart_data)


chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(chart_data).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

st.altair_chart(c, use_container_width=True)

###

from vega_datasets import data

source = data.seattle_weather()

scale = alt.Scale(
    domain=["sun", "fog", "drizzle", "rain", "snow"],
    range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"],
)
color = alt.Color("weather:N", scale=scale)

# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])

# Top panel is scatter plot of temperature vs time
points = (
    alt.Chart()
    .mark_point()
    .encode(
        alt.X("monthdate(date):T", title="Date"),
        alt.Y(
            "temp_max:Q",
            title="Maximum Daily Temperature (C)",
            scale=alt.Scale(domain=[-5, 40]),
        ),
        color=alt.condition(brush, color, alt.value("lightgray")),
        size=alt.Size("precipitation:Q", scale=alt.Scale(range=[5, 200])),
    )
    .properties(width=550, height=300)
    .add_selection(brush)
    .transform_filter(click)
)

# Bottom panel is a bar chart of weather type
bars = (
    alt.Chart()
    .mark_bar()
    .encode(
        x="count()",
        y="weather:N",
        color=alt.condition(click, color, alt.value("lightgray")),
    )
    .transform_filter(brush)
    .properties(
        width=550,
    )
    .add_selection(click)
)

chart = alt.vconcat(points, bars, data=source, title="Seattle Weather: 2012-2015")

st.altair_chart(chart, theme="streamlit", use_container_width=True)


###

with tab2:
    with st.form(key='params_for_api1'):
        query = st.text_input('Input topic or notion to get most relevent papers:')
        st.form_submit_button('Browse the arXiv net!')


with tab3:
    with st.form(key='params_for_api2'):
        query = st.text_input('Input topic or notion to get most relevent papers:')
        st.form_submit_button('Browse the arXiv net!')