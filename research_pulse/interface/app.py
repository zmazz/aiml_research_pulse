#import datetime
import requests
# import research_pulse.logic.search as ls

import streamlit as st
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#import plotly.express as px
#import research_pulse.logic.data_loader as ldl
#import research_pulse.logic.analytics_agg as laa
import streamlit.components.v1 as components
from base64 import b64encode
from io import BytesIO

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

# def displayPDF(file):
#     # Opening file from file path
#     # with open(file, "rb") as f:
#     base64_pdf = b64encode(file).decode('utf-8')

#     # Embedding PDF in HTML
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" ' \
#                   F'width="100%" height="1000" type="application/pdf"></iframe>'
#     # Displaying File
#     return st.markdown(pdf_display, unsafe_allow_html=True)

# top30_papers={'id': {46748: '1004-3169',
#   259652: '1612-07324',
#   61245: '1101-0618',
#   309974: '1712-03107',
#   10529: '801-2826',
#   184148: '1503-00732',
#   335256: '1805-04405',
#   311063: '1712-05815',
#   115231: '1302-028',
#   70818: '1106-1445',
#   435035: '1909-11512',
#   91715: '1204-245',
#   115422: '1302-0884',
#   330983: '1804-06469',
#   374264: '1812-02893',
#   391832: '1903-05082',
#   251952: '1610-08526',
#   303649: '1711-00394',
#   44463: '1003-1366',
#   67673: '1104-3712',
#   302087: '1710-08425',
#   172135: '1410-8712',
#   45407: '1003-4725',
#   394362: '1903-10563',
#   336141: '1805-06467',
#   454388: '1912-06855',
#   380995: '1901-05895',
#   211098: '1511-04265',
#   237666: '1606-08953',
#   346227: '1807-03334'},
#  'title': {46748: 'Factorizations of Cunningham numbers with bases 13 to 99',
#   259652: 'Holographic quantum matter',
#   61245: 'Gauge/String Duality, Hot QCD and Heavy Ion Collisions',
#   309974: 'Dynamical systems applied to cosmology: dark energy and modified gravity',
#   10529: 'Non-Commutative Geometry, Categories and Quantum Physics',
#   184148: 'Quantum field theory in a magnetic field: From quantum chromodynamics to\n  graphene and Dirac semimetals',
#   335256: 'The Conformal Bootstrap: Theory, Numerical Techniques, and Applications',
#   311063: 'Relativistic Fluid Dynamics In and Out of Equilibrium -- Ten Years of\n  Progress in Theory and Numerical Simulations of Nuclear Collisions',
#   115231: 'Holographic applications of logarithmic conformal field theories',
#   70818: 'From Classical to Quantum Shannon Theory',
#   435035: 'Synthetic Data for Deep Learning',
#   91715: 'Entanglement Entropy from a Holographic Viewpoint',
#   115422: 'Scale invariance vs conformal invariance',
#   330983: 'Bayesian parameter estimation for relativistic heavy-ion collisions',
#   374264: 'The Calabi-Yau Landscape: from Geometry, to Physics, to Machine-Learning',
#   391832: 'Machine Learning Solutions for High Energy Physics: Applications to\n  Electromagnetic Shower Generation, Flavor Tagging, and the Search for\n  di-Higgs Production',
#   251952: 'BMS Particles in Three Dimensions',
#   303649: 'Universal gradient descent',
#   44463: 'Fundamentals of the Exact Renormalization Group',
#   67673: 'Entanglement entropy of black holes',
#   302087: 'Hydrodynamics of electrons in graphene',
#   172135: 'Functional renormalisation approach to driven dissipative dynamics',
#   45407: 'Quantum integrability and functional equations',
#   394362: 'Machine learning and the physical sciences',
#   336141: 'Top Down Approach to 6D SCFTs',
#   454388: 'Planar maps and random partitions',
#   380995: 'Bipartite Quantum Interactions: Entangling and Information Processing\n  Abilities',
#   211098: 'Eisenstein series and automorphic representations',
#   237666: 'TASI lectures on quantum matter (with a view toward holographic duality)',
#   346227: 'An introduction to the SYK model'},
#  'authors': {46748: 'Brent Richard P., Montgomery Peter L., Riele Herman J. J. te',
#   259652: 'Hartnoll Sean A., Lucas Andrew, Sachdev Subir',
#   61245: 'Casalderrey-Solana Jorge, Liu Hong, Mateos David, Rajagopal Krishna, Wiedemann Urs Achim',
#   309974: 'Bahamonde Sebastian, Boehmer Christian G., Carloni Sante, Copeland Edmund J., Fang Wei, Tamanini Nicola',
#   10529: 'Bertozzini Paolo, Conti Roberto, Lewkeeratiyutkul Wicharn',
#   184148: 'Miransky Vladimir A., Shovkovy Igor A.',
#   335256: 'Poland David, Rychkov Slava, Vichi Alessandro',
#   311063: 'Romatschke Paul, Romatschke Ulrike',
#   115231: 'Grumiller D., Riedler W., Rosseel J., Zojer T.',
#   70818: 'Wilde Mark M.',
#   435035: 'Nikolenko Sergey I.',
#   91715: 'Takayanagi Tadashi',
#   115422: 'Nakayama Yu',
#   330983: 'Bernhard Jonah E.',
#   374264: 'He Yang-Hui',
#   391832: 'Paganini Michela',
#   251952: 'Oblak Blagoje',
#   303649: 'Gasnikov Alexander',
#   44463: 'Rosten Oliver J.',
#   67673: 'Solodukhin Sergey N.',
#   302087: 'Lucas Andrew, Fong Kin Chung',
#   172135: 'Mathey Steven',
#   45407: 'Volin Dmytro',
#   394362: 'Carleo Giuseppe, Cirac Ignacio, Cranmer Kyle, Daudet Laurent, Schuld Maria, Tishby Naftali, Vogt-Maranto Leslie, Zdeborová Lenka',
#   336141: 'Heckman Jonathan J., Rudelius Tom',
#   454388: 'Bouttier Jérémie',
#   380995: 'Das Siddhartha',
#   211098: 'Fleig Philipp, Gustafsson Henrik P. A., Kleinschmidt Axel, Persson Daniel',
#   237666: 'McGreevy John',
#   346227: 'Rosenhaus Vladimir'},
#  'url': {46748: 'https://arxiv.org/pdf/1004.3169.pdf',
#   259652: 'https://arxiv.org/pdf/1612.07324.pdf',
#   61245: 'https://arxiv.org/pdf/1101.0618.pdf',
#   309974: 'https://arxiv.org/pdf/1712.03107.pdf',
#   10529: 'https://arxiv.org/pdf/0801.2826.pdf',
#   184148: 'https://arxiv.org/pdf/1503.00732.pdf',
#   335256: 'https://arxiv.org/pdf/1805.04405.pdf',
#   311063: 'https://arxiv.org/pdf/1712.05815.pdf',
#   115231: 'https://arxiv.org/pdf/1302.0280.pdf',
#   70818: 'https://arxiv.org/pdf/1106.1445.pdf',
#   435035: 'https://arxiv.org/pdf/1909.11512.pdf',
#   91715: 'https://arxiv.org/pdf/1204.2450.pdf',
#   115422: 'https://arxiv.org/pdf/1302.0884.pdf',
#   330983: 'https://arxiv.org/pdf/1804.06469.pdf',
#   374264: 'https://arxiv.org/pdf/1812.02893.pdf',
#   391832: 'https://arxiv.org/pdf/1903.05082.pdf',
#   251952: 'https://arxiv.org/pdf/1610.08526.pdf',
#   303649: 'https://arxiv.org/pdf/1711.00394.pdf',
#   44463: 'https://arxiv.org/pdf/1003.1366.pdf',
#   67673: 'https://arxiv.org/pdf/1104.3712.pdf',
#   302087: 'https://arxiv.org/pdf/1710.08425.pdf',
#   172135: 'https://arxiv.org/pdf/1410.8712.pdf',
#   45407: 'https://arxiv.org/pdf/1003.4725.pdf',
#   394362: 'https://arxiv.org/pdf/1903.10563.pdf',
#   336141: 'https://arxiv.org/pdf/1805.06467.pdf',
#   454388: 'https://arxiv.org/pdf/1912.06855.pdf',
#   380995: 'https://arxiv.org/pdf/1901.05895.pdf',
#   211098: 'https://arxiv.org/pdf/1511.04265.pdf',
#   237666: 'https://arxiv.org/pdf/1606.08953.pdf',
#   346227: 'https://arxiv.org/pdf/1807.03334.pdf'},
#  'year': {46748: 2010,
#   259652: 2018,
#   61245: 2012,
#   309974: 2018,
#   10529: 2011,
#   184148: 2015,
#   335256: 2019,
#   311063: 2019,
#   115231: 2013,
#   70818: 2019,
#   435035: 2019,
#   91715: 2012,
#   115422: 2014,
#   330983: 2018,
#   374264: 2020,
#   391832: 2019,
#   251952: 2018,
#   303649: 2018,
#   44463: 2012,
#   67673: 2011,
#   302087: 2018,
#   172135: 2015,
#   45407: 2010,
#   394362: 2019,
#   336141: 2019,
#   454388: 2019,
#   380995: 2019,
#   211098: 2016,
#   237666: 2016,
#   346227: 2018},
#  'num_cit': {46748: 1266,
#   259652: 626,
#   61245: 568,
#   309974: 534,
#   10529: 505,
#   184148: 492,
#   335256: 421,
#   311063: 368,
#   115231: 268,
#   70818: 257,
#   435035: 229,
#   91715: 222,
#   115422: 218,
#   330983: 208,
#   374264: 201,
#   391832: 197,
#   251952: 194,
#   303649: 186,
#   44463: 185,
#   67673: 184,
#   302087: 180,
#   172135: 180,
#   45407: 177,
#   394362: 176,
#   336141: 173,
#   454388: 172,
#   380995: 172,
#   211098: 164,
#   237666: 162,
#   346227: 159}}

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
    Aggregates, Rankings, Categories = Search.tabs(["Aggregates","Rankings","by Category (soon)"])
    with Aggregates:
        # col1, col2= st.columns(2)
        # with col1 :
        #     st.image('https://storage.googleapis.com/deepdipper_data/images/1-Numbers-of-Publications-per-Year.png', caption='Numbers of Publications per Year', use_column_width=True)
        # with col2 :
        #     st.image('https://storage.googleapis.com/deepdipper_data/images/2-Number-of-Publications-by-Year-and-Categ.png', caption='Numbers of Publications by year and by category', use_column_width=True)
        st.markdown("<h6 style='text-align: center; color: #289c68'>Aggregate number of papers per year:</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/aggregate/agg_number_papers_year.png', caption='Number of papers per year', use_column_width=True)
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Aggregate number of papers & citations per year:</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/aggregate/agg_number_public_citations.png', caption='Number of papers and citations per year', use_column_width=True)

    with Rankings:
        st.markdown("<h6 style='text-align: center; color: #289c68'>Top 30 most cited authors:</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/ranking/top_30_cited_authors.png', caption='Ranked authors by citations', use_column_width=True)
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Top 30 most cited papers:</h6>", unsafe_allow_html=True)
        #st.write(pd.DataFrame(top30_papers))
        st.markdown("  ")
        st.markdown("<h6 style='text-align: center; color: #289c68'>Top 20 categories with most papers:</h6>", unsafe_allow_html=True)
        st.image('https://storage.googleapis.com/deepdipper_data/images/ranking/top_20_categories.png', caption='Ranked authors by citations', use_column_width=True)

    with Categories:
        st.text(' ')
        st.markdown('-- coming soon, stay tuned! --')

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

                response3 = requests.get(research_pulse_api_url3, params=dict(query=params3))

                results3 = response3.json()


                for key in results3:
                    st.markdown('--- ' + str(results3[key]['Title']) + ' ---')
                    st.markdown('By : ' + str(results3[key]['Authors']))
                    st.markdown('Cited ' + str(results3[key]['Number_citations']) + ' times -- Published in ' + str(results3[key]['Year']))
                    st.markdown('arXiv category : ' + str(results3[key]['Category']) + ' -- Paper ID : ' + str(results3[key]['Id']))

                    st.text(' ')
                    st.text(' ')

                for key in results3:
                    pdf_url = results3[key]['Link']
                    #displayPDF(pdf_url)

                    # pdf_viewer = f'<iframe src="{pdf_url}" width="600" height="800"></iframe>'
                    # st.markdown(pdf_viewer, unsafe_allow_html=True)
                    # with open(pdf_url, 'rb') as f:
                    #     base64_pdf = b64encode(f.read()).decode('utf-8')

                    # pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf"></iframe>'

                    # pdf_display = F'<iframe src="{pdf_url}" width="700" height="900" type="application/pdf"></iframe>'
                    # st.markdown(pdf_display, unsafe_allow_html=True)
                    # # st.markdown(pdf_display, unsafe_allow_html=True)
                    # response_pdf = requests.get(pdf_url)

                    # # Read the downloaded binary data into a BytesIO object
                    # pdf_data = BytesIO(response_pdf.content)
                    # # Generate the HTML code to display the PDF
                    # base64_pdf = b64encode(pdf_data.read()).decode('utf-8')
                    # # Display the PDF
                    # st.markdown(f'<embed src="data:application/pdf;base64,{base64_pdf}" width="600" height="800" type="application/pdf">', unsafe_allow_html=True)


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
