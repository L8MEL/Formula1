import streamlit as st

from pages.helper.sets import session_selection, sideBarLayout
from pages.helper.helper import getSession

st.set_page_config(page_title='F1 Timing', layout='wide')

if not 'track' in st.session_state:
    print('Setting defaul values')
    st.session_state['track'] = 'Melbourne'
    st.session_state['year'] = 2022
    st.session_state['event_type'] = 'Race'

#st.session_state['data_loaded_successful'] = False

st.title('Welcome to the F1 Data Analysis Page')

args = session_selection()
st.button(label='Load Session', on_click=getSession, args=args)

try:
    session = st.session_state['session']
    st.session_state['data_loaded'] = True
    st.success('Data successfully loaded')
except:
    st.session_state['data_loaded'] = False
    st.error("No data loaded")

sideBarLayout()



