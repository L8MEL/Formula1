import streamlit as st
from pages.helper.lapAnalysisHelper import *
from pages.helper.sets import sideBarLayout

session = st.session_state['session']

sideBarLayout()

st.title('Lap Analyser')
selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']),
                                  default=pd.unique(session.laps['Driver'])[0])
values = ['SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'Sector1Time']
speedTrap = st.selectbox(label='Speedtrap selector', options=values)

try:
    df = getSpeedTrapDf(session, selected_drivers, speedTrap)
except Exception as e:
    st.error("Data could not be combined!")

try:
    plotDf(df, selected_drivers, speedTrap)
except Exception as e:
    st.error('An error occured')

