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



st.set_page_config(
    page_title="ResPulse",
    page_icon=":smiley:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "AI, ML and related research areas are evolving at a rapid pace. Research Pulse is a tool that helps you to explore the research papers and their authors. It is a NLP tool that helps you to find the most relevant papers and authors in your research area."
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
st.markdown("<h3 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ  Rᴇsᴇᴀʀcʜ Puʟsᴇ  ﮩ٨ـﮩﮩ٨ـ</h3>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: grey'>NLP tools to master your exploration of research paper</h5>", unsafe_allow_html=True)

with st.container():
    About, Search, Research, Dashboard, Tools = st.tabs(["About","- Search engine -","- Research authors or papers -","- Analytics dashboard -","- NLP-assistive tools -"])

    with About:
        st.markdown(' ')
        st.markdown("AI, ML and related research areas are evolving at a rapid pace.", unsafe_allow_html=True)
        st.markdown("Research Pulse is a tool that helps you to explore the research papers and their authors", unsafe_allow_html=True)
        st.markdown("It is a NLP tool that helps you to find the most relevant papers and authors in your research area", unsafe_allow_html=True)
        st.markdown(' ')
        st.markdown("<h6 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ Search engine ﮩ٨ـﮩﮩ٨ـ</h6>", unsafe_allow_html=True)
        st.markdown("Curated dataset of 774k research papers in areas related by close or by far to AI/ML.", unsafe_allow_html=True)
        st.markdown("Corpus of research papers published after 2000 and openly available on arXiv.org", unsafe_allow_html=True)
        st.markdown(' ')
        st.markdown("<h6 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ Research papers & authors ﮩ٨ـﮩﮩ٨ـ</h6>", unsafe_allow_html=True)
        st.markdown("Look for a paper by inputting its ID.", unsafe_allow_html=True)
        st.markdown("Look for an author by inputting his/her name.", unsafe_allow_html=True)
        st.markdown("--tobedone: citation network graph parser, codes & algos repository per category...", unsafe_allow_html=True)
        st.markdown(' ')
        st.markdown("<h6 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ tobedone: Analytics dashboard ﮩ٨ـﮩﮩ٨ـ</h6>", unsafe_allow_html=True)
        st.markdown("Set of analytics views on the database.", unsafe_allow_html=True)
        st.markdown("Available for all papers, by category, by year filtrage, with key metrics dissected.", unsafe_allow_html=True)
        st.markdown(' ')
        st.markdown("<h6 style='text-align: center; color: yellow'>ﮩ٨ـﮩﮩ٨ـ tobedone: NLP-based tools ﮩ٨ـﮩﮩ٨ـ</h6>", unsafe_allow_html=True)
        st.markdown("Set of tools to help in the exploration of research areas.", unsafe_allow_html=True)
        st.markdown("--tobedone: translation, summarization, bot alert tool...", unsafe_allow_html=True)

    with Search:
        st.markdown("<h6 style='text-align: center; color: white'>Search topics and notions to get top 20 most relevant papers :</h6>", unsafe_allow_html=True)
        with st.form(key='params_for_api_search') as search_form:
            input1 = st.text_input('> input 1 to 5 keywords of interest separated by space')
            if st.form_submit_button('Search for papers!'):

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

    with Research:
        st.markdown("<h6 style='text-align: center; color: white'>Research authors and papers to get info on them:</h6>", unsafe_allow_html=True)
        Authors,Papers = Research.tabs(["Authors - by name","Papers - by ID"])

        with Authors:
            with st.form(key='params_for_api_authors'):

                input2 = st.text_input('> input author name to get detailed info on them')

                if st.form_submit_button('Research Author!'):

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

        with Papers:
            with st.form(key='params_for_api_papers'):

                input3 = st.text_input('> input paper ID to get detailed info on it (e.g. 2023-12345)')

                if st.form_submit_button('Research Paper!'):

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

                    for key in results3:
                        st.markdown('-- ' + str(results3[key]['Title']) + ', cited ' + str(results3[key]['Number_citations']) + ' times')
                        st.markdown(str(results3[key]['Year'])+ ', ' + str(results3[key]['Authors']) + ', ' + str(results3[key]['Link']))
                        st.markdown('Paper ID: ' + str(results3[key]['Id'])+ ' -- Category: ' + str(results3[key]['Category']))
                        st.text('ABSTRACT -- ' + str(results3[key]['Abstract']))
                        st.text(' ')
                        st.text(' ')

        with Dashboard:
            st.markdown('-- coming soon, stay tuned! --')

        with Tools:
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
