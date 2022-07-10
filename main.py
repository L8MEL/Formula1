import streamlit as st

from pages.helper.sets import session_selection
from pages.helper.helper import getSession

st.set_page_config(page_title='F1 Timing', layout='wide')

if ['track', 'year', 'event_type'] not in st.session_state:
    st.session_state['track'] = 'Melbourne'
    st.session_state['year'] = 2022
    st.session_state['event_type'] = 'Race'

#st.session_state['data_loaded_successful'] = False

st.title('Welcome to the F1 Data Analysis Page')

session_selection()
st.button(label='Load Session', on_click=getSession, args=(st.session_state['track'], st.session_state['year'],
                                                           st.session_state['event_type']))

try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data loaded. \n Please load a session")

if data_loaded:
    st.subheader('Data is loaded succesfully')



