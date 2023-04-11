import streamlit as st

import datetime
import requests
# import research_pulse.logic.search as ls

'''
# AI/ML Research Pulse

'''
st.text('--- Research papers search engine ---')
st.text('Curated dataset of 774k research papers in areas related by close or by far to AI/ML')
st.text('Corpus of research papers published after 2000 and openly available on arXiv.org')
st.text('')
with st.form(key='params_for_api'):

    input = st.text_input('Please input topic or notion to get most relevent papers:')

    if st.form_submit_button('Browse the arXiv net!'):

        params = input.replace(' ','-').lower()

        #research_pulse_api_url = 'http://127.0.0.1:8000/search?query='
        research_pulse_api_url = 'https://deepdipper-rp6v7d7m4q-ew.a.run.app/search'

        #response = requests.get(research_pulse_api_url+params)
        response = requests.get(research_pulse_api_url, params=dict(query=params))

        results = response.json()

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
            st.markdown(f'#{i+1} -- ' + results[k]['Title'])
            st.markdown(str(results[k]['Year'])+ ', ' + str(results[k]['Authors']) + ', ' + results[k]['Link'])
            st.text('ABSTRACT -- ' + results[k]['Abstract'])
            st.text('')
