import streamlit as st

import datetime
import requests
import research_pulse.logic.search as ls

'''
## AI/ML Research Pulse

'''
st.text('--- AI/ML search engine ---')
st.text('Curated dataset of 774k research papers in areas related by close or by far to AI/ML')
st.text('Corpus of research papers published after 2000 and openly available on arXiv.org')
st.text('')
with st.form(key='params_for_api'):

    query = st.text_input('Input a topic related to AI/ML to get the top 5 most relevent research papers on it:')

    st.form_submit_button('Browse the arXiv net!')

#params = dict(query=query)

#research_pulse_api_url = 'https://XXXXXX/search'
#response = requests.get(research_pulse_api_url, params=params)

#search = response.json()

data=ls.load_data()
vector, matrix = ls.vectorizer(data)

results = ls.search(query=query, data=data, vector=vector, matrix=matrix)

st.header('Top result:')
st.markdown('#1 -- ' + results[0]['Title'])
st.markdown('author(s): ' + str(results[0]['Authors']))
st.markdown('published on arXiv in '+ str(results[0]['Year']) + ' ' + ' ---  ' + ' ' + ' url: ' + results[0]['Link'])
st.text('abstract -- ' + results[0]['Abstract'])
st.text('')
st.text('--------------------------------------------------------------------------------')
st.text('')
st.markdown('#2 -- ' + results[1]['Title'])
st.markdown('author(s): ' + str(results[1]['Authors']))
st.markdown('published on arXiv in '+ str(results[1]['Year']) + ' ' + ' ---  ' + ' ' + ' url: ' + results[1]['Link'])
st.text('abstract -- ' + results[1]['Abstract'])
st.text('')
st.text('--------------------------------------------------------------------------------')
st.text('')
st.markdown('#3 -- ' + results[2]['Title'])
st.markdown('author(s): ' + str(results[2]['Authors']))
st.markdown('published on arXiv in '+ str(results[2]['Year']) + ' ' + ' ---  ' + ' ' + ' url: ' + results[2]['Link'])
st.text('abstract -- ' + results[2]['Abstract'])
st.text('')
st.text('--------------------------------------------------------------------------------')
st.text('')
st.markdown('#4 -- ' + results[3]['Title'])
st.markdown('author(s): ' + str(results[3]['Authors']))
st.markdown('published on arXiv in '+ str(results[3]['Year']) + ' ' + ' ---  ' + ' ' + ' url: ' + results[3]['Link'])
st.text('abstract -- ' + results[3]['Abstract'])
st.text('')
st.text('--------------------------------------------------------------------------------')
st.text('')
st.markdown('#5 -- ' + results[4]['Title'])
st.markdown('author(s): ' + str(results[4]['Authors']))
st.markdown('published on arXiv in '+ str(results[4]['Year']) + ' ' + ' ---  ' + ' ' + ' url: ' + results[4]['Link'])
st.text('abstract -- ' + results[4]['Abstract'])
st.text('')
st.text('--------------------------------------------------------------------------------')
