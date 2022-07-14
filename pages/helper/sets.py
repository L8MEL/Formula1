from pages.helper.helper import *
import streamlit as st
from pages.helper.dataManager import DataManager


def session_selection():
    grandPrix = ['Melbourne', 'Singapore', 'Spielberg', 'Spa', 'Barcelona', 'Silverstone']

    year_list = list(range(2022, 2000, -1))
    session_list = ['Race', 'Qualifying', 'FP1', 'FP2', 'FP3']
    # Page Layout
    st.subheader("Select Event")
    selected_track = st.selectbox(label="Drivers", options=grandPrix,
                                  index=grandPrix.index(st.session_state['track']))
    selected_year = st.selectbox(label="Year", options=year_list,
                                 index=year_list.index(st.session_state['year']))
    selected_session = st.selectbox(label="Session", options=session_list,
                                    index=session_list.index(st.session_state['event_type']))

    return selected_year, selected_track,  selected_session

def sideBarLayout():
    with st.sidebar:
        if "data_manager" in st.session_state:
            manager: DataManager = st.session_state['data_manager']
            if manager.loaded_data:
                st.text('Track: ' + st.session_state['track'])
                st.text('Year: ' + str(st.session_state['year']))
                st.text('Session: ' + st.session_state['event_type'])

                st.metric(label='Air Temperature', value=str(manager.airTemp_mean) + ' °C')
                st.metric(label='Humidity', value=str(manager.humidity_mean) + ' %')
                st.metric(label='Track Temperature', value=str(manager.trackTemp_mean) + ' °C')
                st.metric(label='Max Windspeed', value=str(manager.windSpeed_max) + ' km/h')


def map():
    st.subheader('Map View')
    fig, ax = plt.subplots(figsize=(16, 8))
    try:
        for driver in selected_drivers:
            if area == 'Fastest':
                x = session.laps.pick_driver(driver).pick_fastest().telemetry['X']
                y = session.laps.pick_driver(driver).pick_fastest().telemetry['Y']
            else:
                x = session.laps.pick_driver(driver).telemetry['X']
                y = session.laps.pick_driver(driver).telemetry['Y']

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            ax.plot(x, y, linewidth=2)

        ax.set_facecolor('#0E1117')
        fig.patch.set_facecolor('#0E1117')
        ax.axis('off')
        ax.legend(selected_drivers)
        print(selected_drivers)

        st.pyplot(fig)