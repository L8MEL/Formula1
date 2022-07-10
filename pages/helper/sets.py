import streamlit as st


def session_selection():
    grandPrix = ['Melbourne', 'Singapore', 'Spielberg', 'Spa', 'Barcelona', 'Silverstone']

    # Page Layout
    st.subheader("Select Event")
    selected_track = st.selectbox(label="Drivers", options=grandPrix)
    selected_year = st.selectbox(label="Year", options=list(range(2022, 2000, -1)))
    selected_session = st.selectbox(label="Session", options=['Race', 'Qualifying', 'FP1', 'FP2', 'FP3'])

    st.session_state['track'] = selected_track
    st.session_state['year'] = selected_year
    st.session_state['event_type'] = selected_session
