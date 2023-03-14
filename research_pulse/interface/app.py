#import datetime
import requests
# import research_pulse.logic.search as ls

import streamlit as st
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import plotly.express as px
#import research_pulse.logic.data_loader as ldl
#import research_pulse.logic.analytics_agg as laa
from streamlit.components.v1 import iframe

st.set_page_config(
    page_title="ResPulse",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/zmazz/aiml_research_pulse',
        'Report a bug': "https://github.com/zmazz/aiml_research_pulse",
        'About': "AI, ML and related research areas are evolving at a rapid pace. Research Pulse is a tool that helps you to explore the research papers and their authors. It is a NLP tool that helps you to find the most relevant papers and authors in your research area. For more info, please contact https://github.com/zmazz."
    }
)

#@st.cache_data
#def load_data():
#    data=ldl.load_data()
#    return data

#df=load_data()

html_temp = """
            <div style="background-color:{};padding:1px">
            </div>
            """

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

#st.markdown("<h3 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ  Ｒｅｓｅａｒｃｈ Ｐｕｌｓｅ  ﮩ٨ـﮩﮩ٨ـ</h3>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #289c68'>ﮩ٨ـﮩﮩ٨ـ   Rᴇsᴇᴀʀcʜ Puʟsᴇ   ﮩ٨ـﮩﮩ٨ـ</h3>", unsafe_allow_html=True)
#st.markdown("<h3 style='text-align: center; color: yellow;'> Research Pulse </h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey;'>NLP-based tools to master the exploration of research papers</h5>", unsafe_allow_html=True)

About, Dashboard, Search, Research, Tools = st.tabs(["About","Dashboard","Search","Research","Tools (soon)"])

with About:
    st.markdown(' ')
    st.markdown("AI, ML and related research areas are evolving at a rapid pace.", unsafe_allow_html=True)
    st.markdown("Research Pulse is a tool that helps in the exploration of research papers and their authors.", unsafe_allow_html=True)
    st.markdown("It is an all-in-one NLP toolkit that helps in finding most relevant insight in large and fast-evolving research areas.", unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown("<h6 style='text-align: center; color: #289c68'>--- Search engine ---</h6>", unsafe_allow_html=True)
    st.markdown("Curated dataset of 774k research papers in areas related by close or by far to AI/ML.", unsafe_allow_html=True)
    st.markdown("Corpus of research papers published after 2000 and openly available on arXiv.org", unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown("<h6 style='text-align: center; color: #289c68'>--- Research papers & authors ---</h6>", unsafe_allow_html=True)
    st.markdown("Look for a paper by inputting its ID.", unsafe_allow_html=True)
    st.markdown("Look for an author by inputting his/her name.", unsafe_allow_html=True)
    st.markdown("--tobedone: citation network graph parser, codes & algos repository per category...", unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown("<h6 style='text-align: center; color: #289c68'>--- Analytics dashboard ---</h6>", unsafe_allow_html=True)
    st.markdown("Set of analytics views on the database.", unsafe_allow_html=True)
    st.markdown("Available for all papers, by category, by year filtrage, with key metrics dissected.", unsafe_allow_html=True)
    st.markdown(' ')
    st.markdown("<h6 style='text-align: center; color: #289c68'>--- NLP-based tools ---</h6>", unsafe_allow_html=True)
    st.markdown("Set of tools to help in the exploration of research areas.", unsafe_allow_html=True)
    st.markdown("--tobedone: translation, summarization, bot alert tool...", unsafe_allow_html=True)

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

with Search:
    st.markdown("<h6 style='text-align: center; color: #289c68'>Search papers and authors to get most relevant content:</h6>", unsafe_allow_html=True)
    Papers,Authors = Search.tabs(["Papers top20 by notions & topics","Author(s) papers by name"])

    with Papers:
        with st.form(key='params_for_api_search_papers') as search_form:
            input1 = st.text_input('\> input one to five keywords of interest separated by space')
            if st.form_submit_button('Search for Papers !'):

                params1 = input1.replace(' ','-').lower()

                #research_pulse_api_url1 = 'http://127.0.0.1:8000/search?query='
                research_pulse_api_url1 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/search'

                #response1 = requests.get(research_pulse_api_url1+params1)
                response1 = requests.get(research_pulse_api_url1, params=dict(query=params1))

                results1 = response1.json()

                #print(results)

                #data=ls.load_data()
                #vector, matrix = ls.vectorizer(data)

                #results = ls.search(query=query, data=data, vector=vector, matrix=matrix)

                #st.header('Top result:')

                '''
                #### Top 20 results:
                '''
                for i in range(0,20):
                    k=f'{i}'
                    st.markdown(f'#{i+1} -- ' + results1[k]['Title'] + ', cited ' + str(results1[k]['Number_citations']) + ' times')
                    st.markdown(str(results1[k]['Year'])+ ', ' + str(results1[k]['Authors']) + ', ' + results1[k]['Link'])
                    st.markdown('Paper ID: ' + str(results1[k]['Id'])+ ' -- Category: ' + str(results1[k]['Category']))
                    st.text('ABSTRACT -- ' + results1[k]['Abstract'])
                    st.text(' ')
                    st.text(' ')

    with Authors:
        with st.form(key='params_for_api_search_authors'):

            input2 = st.text_input('\> input name to get all papers from authors containing this name')

            if st.form_submit_button('Search for Authors !'):

                params2 = input2.replace(' ','-').lower()

                #research_pulse_api_url2 = 'http://127.0.0.1:8000/authors?query='
                research_pulse_api_url2 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/authors'

                #response2 = requests.get(research_pulse_api_url2+params2)
                response2 = requests.get(research_pulse_api_url2, params=dict(query=params2))

                results2 = response2.json()

                for key in results2:
                    st.markdown('-- ' + str(results2[key]['Title']) + ', cited ' + str(results2[key]['Number_citations']) + ' times')
                    st.markdown(str(results2[key]['Year'])+ ', ' + str(results2[key]['Authors']) + ', ' + str(results2[key]['Link']))
                    st.markdown('Paper ID: ' + str(results2[key]['Id'])+ ' -- Category: ' + str(results2[key]['Category']))
                    st.text('ABSTRACT -- ' + str(results2[key]['Abstract']))
                    st.text(' ')
                    st.text(' ')

with Research:
    st.markdown("<h6 style='text-align: center; color: #289c68'>Research authors and papers to get info on them:</h6>", unsafe_allow_html=True)
    Paper_details,Author_details = Research.tabs(["Papers' details by ID","Author's details by name"])

    with Paper_details:
        with st.form(key='params_for_api_research_paper'):

            input3 = st.text_input('\> input exact paper ID to get detailed info on it (e.g. 1903-06236)')

            if st.form_submit_button('Research Paper !'):

                params3 = input3.replace(' ','-').lower()


                #research_pulse_api_url3 = 'http://127.0.0.1:8000/papers?query='
                research_pulse_api_url3 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/papers'

                #response3 = requests.get(research_pulse_api_url3+params3)
                response3 = requests.get(research_pulse_api_url3, params=dict(query=params3))

                results3 = response3.json()

                # for key in results3.keys():
                #     st.markdown('-- ' + results3[key]['Title'])
                #     st.markdown(str(results3[key]['Year'])+ ', ' + str(results3[key]['Authors']) + ', ' + results3[key]['Link'])
                #     st.text('ABSTRACT -- ' + results3[key]['Abstract'])
                #     st.text('')

                col7, col8= st.columns(2)
                with col7 :
                    for key in results3:
                        st.markdown('--- ' + str(results3[key]['Title']) + ' ---')
                        st.markdown('- Cited ' + str(results3[key]['Number_citations']) + ' times -- Published in ' + str(results3[key]['Year']))
                        st.markdown('- Authors :' + str(results3[key]['Authors']))
                        st.markdown('- arXiv category : ' + str(results3[key]['Category']) + '-- Paper ID: ' + str(results3[key]['Id']))
                        st.text('ABSTRACT -- ' + str(results3[key]['Abstract']))
                        st.text(' ')
                        st.text(' ')
                with col8 :
                    for key in results3:
                        pdf_url = results3[key]['Link']
                        # Use pdfjs to display the PDF
                        pdf_viewer = iframe(src=pdf_url, width=600, height=800)
                        # Display the PDF viewer
                        st.write(pdf_viewer)
                        #st.markdown(f'<iframe src="{pdf_url}" width="600" height="800" frameborder="0"></iframe>', unsafe_allow_html=True)

    with Author_details:
        with st.form(key='params_for_api_research_author'):

            input4 = st.text_input('\> input exact author name to get detailed info on them (e.g. Chollet Francois)')

            if st.form_submit_button('Research Author !'):

                params4 = input4.replace(' ','-').lower()

                #research_pulse_api_url4 = 'http://127.0.0.1:8000/authors?query='
                research_pulse_api_url4 = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/authors'

                #response4 = requests.get(research_pulse_api_url4+params4)
                response4 = requests.get(research_pulse_api_url4, params=dict(query=params4))

                results4 = response4.json()

                for key in results4:
                    st.markdown('-- ' + str(results4[key]['Title']) + ', cited ' + str(results4[key]['Number_citations']) + ' times')
                    st.markdown(str(results4[key]['Year'])+ ', ' + str(results4[key]['Authors']) + ', ' + str(results4[key]['Link']))
                    st.markdown('Paper ID: ' + str(results4[key]['Id'])+ ' -- Category: ' + str(results4[key]['Category']))
                    st.text('ABSTRACT -- ' + str(results4[key]['Abstract']))
                    st.text(' ')
                    st.text(' ')

with Tools:
    st.text(' ')
    st.markdown('-- coming soon, stay tuned! --')

# with Dashboard:
#     #First row - overall and top50 view
#     Overall, Top50 = Dashboard.tabs(["Overall", "Top50"])

#     with Overall:
#         col1, col2, col3= st.columns([5,5,5])
#         Overall.subheader("Reserved for the overall view of the data")
#         Overall.pyplot(laa.plot_publications_per_year(laa.get_publications_by_time_range(laa.get_publications_per_year(df), 2000, 2023)))
#         col4, col5, col6= st.columns([5,5,5])
#         Overall.subheader("Reserved for the overall view of the data")

#         Overall.write(df)

#         #Second row - interactive view
#         Overall.header("Interactive View")

#         # -- Get the user input
#         year_col, category_col, log_x_col = Overall.columns([5, 5, 5])
#         with year_col:
#             year_choice = Overall.slider(
#                 "What year would you like to examine?",
#                 min_value=2000,
#                 max_value=2023,
#                 step=1,
#                 value=2023,
#             )
#         with category_col:
#             category_choice = Overall.selectbox(
#                 "Which category would you like to look at?",
#                 ("All", 'cond-mat.dis-nn','cond-mat.stat-mech','cond-mat.str-el','cs.AI',
#                     'cs.CE','cs.CG','cs.CL','cs.CR','cs.CV','cs.CY','cs.DB','cs.DC',
#                     'cs.DL','cs.DM','cs.DS','cs.ET','cs.FL','cs.GL','cs.GT','cs.HC',
#                     'cs.IR','cs.IT','cs.LG','cs.LO','cs.MA','cs.MS','cs.NA','cs.NE',
#                     'cs.NI','cs.RO','cs.SI','econ.EM','eess.AS','eess.IV','eess.SP',
#                     'math.CA','math.CT','math.DS','math.FA','math.GN','math.NA',
#                     'math.OC','math.PR','math.RT','math.ST','nlin.AO','nlin.CD',
#                     'stat.AP','stat.CO','stat.ME','stat.ML','stat.OT','stat.TH'))

#         with log_x_col:
#             log_x_choice = Overall.checkbox("Log X Axis?")

#         # -- Apply the year filter given by the user

#         filtered_df = df.loc[(df['year'] >= int(year_choice))]
#         # -- Apply the continent filter
#         if category_choice != "All":
#             filtered_df = filtered_df.loc[filtered_df['category'].str.contains(category_choice.str)]

#         # -- Create the figure in Plotly
#         fig = px.scatter(
#             filtered_df,
#             x="year",
#             y="lifeExp",
#             size="pop",
#             color="continent",
#             hover_name="country",
#             log_x=log_x_choice,
#             size_max=60)
#         fig.update_layout(title="GDP per Capita vs. Life Expectancy")
#         # -- Input the Plotly chart to the Streamlit interface
#         Overall.plotly_chart(fig, use_container_width=True)
#         #The end of the interactive view

#         #Third row - Last 3 months view in global and category perspective
#         Overall.header("Last 3 months view in global and category perspective")

#         Global_view, Cat_view= Overall.tabs(["Global View", "Categorical View"])

#         with Global_view:
#             col1, col2, col3= Global_view.columns([5,5,5])
#             Global_view.subheader("Reserved for the global view of the data")
#             col4, col5, col6= Global_view.columns([5,5,5])
#             Global_view.subheader("Reserved for the global view of the data")

#         with Cat_view:
#             col1, col2, col3= Cat_view.columns([5,5,5])
#             Cat_view.subheader("Reserved for the categorical view of the data")
#             col4, col5, col6= Cat_view.columns([5,5,5])
#             Cat_view.subheader("Reserved for the categorical view of the data")



#         #End of Overall view

#     with Top50:
#             col1, col2, col3= st.columns([5,5,5])
#             Top50.subheader("Reserved for the top50 view of the data")
#             col4, col5, col6= st.columns([5,5,5])
#             Top50.subheader("Reserved for the top50 view of the data")

#             Top50.write(df.head(50))





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
