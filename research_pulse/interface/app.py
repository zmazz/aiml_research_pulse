import streamlit as st

import datetime
import requests
import research_pulse.logic.search as ls

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
        st.markdown('#1 -- ' + results['#1']['Title'])
        st.markdown(str(results['#1']['Year'])+ ', ' + str(results['#1']['Authors']) + ', ' + results['#1']['Link'])
        st.text('ABSTRACT -- ' + results['#1']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#2 -- ' + results['#2']['Title'])
        st.markdown(str(results['#2']['Year'])+ ', ' + str(results['#2']['Authors']) + ', ' + results['#2']['Link'])
        st.text('ABSTRACT -- ' + results['#2']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#3 -- ' + results['#3']['Title'])
        st.markdown(str(results['#3']['Year'])+ ', ' + str(results['#3']['Authors']) + ', ' + results['#3']['Link'])
        st.text('ABSTRACT -- ' + results['#3']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#4 -- ' + results['#4']['Title'])
        st.markdown(str(results['#4']['Year'])+ ', ' + str(results['#4']['Authors']) + ', ' + results['#4']['Link'])
        st.text('ABSTRACT -- ' + results['#4']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#5 -- ' + results['#5']['Title'])
        st.markdown(str(results['#5']['Year'])+ ', ' + str(results['#5']['Authors']) + ', ' + results['#5']['Link'])
        st.text('ABSTRACT -- ' + results['#5']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#6 -- ' + results['#6']['Title'])
        st.markdown(str(results['#6']['Year'])+ ', ' + str(results['#6']['Authors']) + ', ' + results['#6']['Link'])
        st.text('ABSTRACT -- ' + results['#6']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#7 -- ' + results['#7']['Title'])
        st.markdown(str(results['#7']['Year'])+ ', ' + str(results['#7']['Authors']) + ', ' + results['#7']['Link'])
        st.text('ABSTRACT -- ' + results['#7']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#8 -- ' + results['#8']['Title'])
        st.markdown(str(results['#8']['Year'])+ ', ' + str(results['#8']['Authors']) + ', ' + results['#8']['Link'])
        st.text('ABSTRACT -- ' + results['#8']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#9 -- ' + results['#9']['Title'])
        st.markdown(str(results['#9']['Year'])+ ', ' + str(results['#9']['Authors']) + ', ' + results['#9']['Link'])
        st.text('ABSTRACT -- ' + results['#9']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#10 -- ' + results['#10']['Title'])
        st.markdown(str(results['#10']['Year'])+ ', ' + str(results['#10']['Authors']) + ', ' + results['#10']['Link'])
        st.text('ABSTRACT -- ' + results['#10']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#11 -- ' + results['#11']['Title'])
        st.markdown(str(results['#11']['Year'])+ ', ' + str(results['#11']['Authors']) + ', ' + results['#11']['Link'])
        st.text('ABSTRACT -- ' + results['#11']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#12 -- ' + results['#12']['Title'])
        st.markdown(str(results['#12']['Year'])+ ', ' + str(results['#12']['Authors']) + ', ' + results['#12']['Link'])
        st.text('ABSTRACT -- ' + results['#12']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#13 -- ' + results['#13']['Title'])
        st.markdown(str(results['#13']['Year'])+ ', ' + str(results['#13']['Authors']) + ', ' + results['#13']['Link'])
        st.text('ABSTRACT -- ' + results['#13']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#14 -- ' + results['#14']['Title'])
        st.markdown(str(results['#14']['Year'])+ ', ' + str(results['#14']['Authors']) + ', ' + results['#14']['Link'])
        st.text('ABSTRACT -- ' + results['#14']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#15 -- ' + results['#15']['Title'])
        st.markdown(str(results['#15']['Year'])+ ', ' + str(results['#15']['Authors']) + ', ' + results['#15']['Link'])
        st.text('ABSTRACT -- ' + results['#15']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#16 -- ' + results['#16']['Title'])
        st.markdown(str(results['#16']['Year'])+ ', ' + str(results['#16']['Authors']) + ', ' + results['#16']['Link'])
        st.text('ABSTRACT -- ' + results['#16']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#17 -- ' + results['#17']['Title'])
        st.markdown(str(results['#17']['Year'])+ ', ' + str(results['#17']['Authors']) + ', ' + results['#17']['Link'])
        st.text('ABSTRACT -- ' + results['#17']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#18 -- ' + results['#18']['Title'])
        st.markdown(str(results['#18']['Year'])+ ', ' + str(results['#18']['Authors']) + ', ' + results['#18']['Link'])
        st.text('ABSTRACT -- ' + results['#18']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#19 -- ' + results['#19']['Title'])
        st.markdown(str(results['#19']['Year'])+ ', ' + str(results['#19']['Authors']) + ', ' + results['#19']['Link'])
        st.text('ABSTRACT -- ' + results['#19']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
        st.text('')
        st.markdown('#20 -- ' + results['#20']['Title'])
        st.markdown(str(results['#20']['Year'])+ ', ' + str(results['#20']['Authors']) + ', ' + results['#20']['Link'])
        st.text('ABSTRACT -- ' + results['#20']['Abstract'])
        st.text('')
        st.text('--------------------------------------------------------------------------------')
