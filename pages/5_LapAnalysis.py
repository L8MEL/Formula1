import streamlit as st
from pages.helper.lapAnalysisHelper import *
from pages.helper.sets import sideBarLayout

session = loadSession()

sideBarLayout()

st.title('Lap Analyser')
selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']),
                                  default=pd.unique(session.laps['Driver'])[0])
values = ['SpeedI1', 'SpeedI2', 'SpeedFL', 'SpeedST', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'LapTime']

speedTrap = st.selectbox(label='Speedtrap selector', options=values)

try:
    df = getSpeedTrapDf(session, selected_drivers, speedTrap)
except Exception as e:
    st.error("Data could not be combined!")
    print(e)

width, height, marker_size, type = plotlySettings(True)

try:
    plotDf(df, width, height, marker_size, type)
except Exception as e:
    st.error('An error occured')
    print(e)

try:
    stint_df = getStints(session, selected_drivers)
    plotStints(stint_df, width, height, marker_size, type, df.Lap.max())

except Exception as e:
    st.error('An error occured in Metric')
    print(e)



