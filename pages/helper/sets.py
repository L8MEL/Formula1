from pages.helper.helper import *
import streamlit as st
import os

from dataManager.RaceInformationManager import RaceInformationManager

def session_selection():
    grandPrix = ['Melbourne', 'Singapore', 'Spielberg', 'Spa', 'Barcelona', 'Silverstone']

    year_list = list(range(2022, 2000, -1))
    session_list = ['Race', 'Qualifying', 'FP1', 'FP2', 'FP3']
    # Page Layout
    st.subheader("Select Event")
    selected_year = st.selectbox(label="Year", options=year_list,
                                 index=year_list.index(st.session_state['year']))

    with st.spinner('Loading Races'):
        race_data = RaceInformationManager(selected_year)

    selected_track = st.selectbox(label="Track", options=race_data.race_info.locality,
                                  index=0)

    selected_session = st.selectbox(label="Session", options=session_list,
                                    index=session_list.index(st.session_state['event_type']))

    return selected_track, selected_year, selected_session


def sideBarLayout():
    with st.sidebar:
        if st.session_state['data_loaded']:
            st.text('Track: ' + st.session_state['track'])
            st.text('Year: ' + str(st.session_state['year']))
            st.text('Session: ' + st.session_state['event_type'])

            df = getWeather(st.session_state['session'])
            st.metric(label='Air Temp.', value=str(round(df.AirTemp.mean(), 1)) + ' °C')
            st.metric(label='Humidity', value=str(int(round(df.Humidity.mean(), 0))) + ' %')
            st.metric(label='Track Temp.', value=str(round(df.TrackTemp.mean(), 1)) + ' °C')
            st.metric(label='Max Windsp.', value=str(round(df.WindSpeed.max(), 1)) + ' km/h')
            st.text('-------------------')

        st.text("Cache Size: %s MB" % str(int(round(get_dir_size('f1_cache')/10**6))))


def plotlySettings(plot_type_selection: bool):
    col1, col2, col3 = st.columns(3)
    width = col1.number_input(label='Width', min_value=100, max_value=2000, value=1200)
    height = col2.number_input(label='Height', min_value=100, max_value=2000, value=800)
    marker_size = col3.number_input(label='Marker Size', min_value=1, max_value=30, value=5)
    plot_type = 'None'
    if plot_type_selection:
        plot_type = st.radio(label='Type', options=['Scatter', 'Line'])

    return width, height, marker_size, plot_type
