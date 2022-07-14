import streamlit as st

from pages.helper.sets import session_selection, sideBarLayout
from pages.helper.helper import getSession

from pages.helper.dataManager import DataManager


def createDataManager(year, track, event_type):
    import pickle
    import glob
    import time
    directory = "result_cache/"
    results = glob.glob(directory + "/*.pickle")
    results = [x.replace(directory, "") for x in results]
    filename = 'dataObject_%s_%s_%s.pickle' %(track, year,
                                              event_type)
    if filename in results:
        print("Result existing")
        with st.spinner("Loading Result"):
            with open(directory + filename, 'br') as file:
                st.session_state['data_manager'] = pickle.load(file)
            #time.sleep(2)

    else:
        print("Calculating new result")
        with st.spinner('Loading and preparing Data'):
            st.session_state['data_manager']: DataManager = DataManager(year, track, event_type)
            if st.session_state['data_manager'].loaded_data:
                with open('result_cache/' + filename, 'bw') as file:
                    pickle.dump(st.session_state['data_manager'], file)


st.set_page_config(page_title='F1 Timing', layout='wide')

if not 'track' in st.session_state:
    st.session_state['track'] = 'Melbourne'
    st.session_state['year'] = 2022
    st.session_state['event_type'] = 'Race'

st.title('Welcome to the F1 Data Analysis Page')
selected_track, selected_year, selected_session = session_selection()
st.button(label='Load Session', on_click=createDataManager, args=(selected_track, selected_year, selected_session) )


if 'data_manager' in st.session_state:
    manager: DataManager = st.session_state['data_manager']
    if manager.loaded_data:
        st.session_state['track'] = manager.track
        st.session_state['year'] = manager.year
        st.session_state['event_type'] = manager.event_type
        st.success('Data succesfully loaded')
    else:
        st.error('No Data available!')
else:
    st.error('No Data available!')

sideBarLayout()
