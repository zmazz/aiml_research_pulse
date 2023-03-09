import streamlit as st

import datetime
import requests
import research_pulse.logic.search as ls

'''
## AI/ML Research Pulse - Search
'''
data=ls.load_data()
vector, matrix = ls.vectorizer(data)

with st.form(key='params_for_api'):

    query = st.text_input('Which topic related to AI/ML do you want research papers on?')

    st.form_submit_button('Look for it!')

#params = dict(query=query)

#research_pulse_api_url = 'https://XXXXXX/search'
#response = requests.get(research_pulse_api_url, params=params)

#search = response.json()

results = ls.search(query=query, data=data, vector=vector, matrix=matrix)

st.markdown(results)
#st.header('Top results:')
#st.header(f'1 - {results[0]} ')
#st.header(f'2 - {results[1]}')
#st.header(f'3 - {results[2]}')
#st.header(f'4 - {results[3]}')
#st.header(f'5 - {results[4]}')
