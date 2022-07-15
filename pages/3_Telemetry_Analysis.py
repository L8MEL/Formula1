import fastf1.core
import fastf1 as f1
import fastf1.plotting
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from pages.helper.helper import *
from pages.helper.telemetry_helper import *

from pages.helper.sets import *
from pages.helper.sets import *

try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.error("No data loaded. \n Please got to main")

if data_loaded:
    sideBarLayout()
    session: fastf1.core.Session = st.session_state['session']
    st.subheader("Results")

    # Driver and Data Selector
    st.subheader("Detailled Analysis")
    selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']),
                                      default=pd.unique(session.laps['Driver'])[0])

    selected_column = st.selectbox(label="Data",
                                   options=session.laps.pick_driver(selected_drivers[0]).get_car_data().columns)

    col1, col2 = st.columns(2)
    area = col1.radio(label="Select Area", options=['Fastest', 'All'])
    plot_type = col2.radio(label="Select Plot", options=['Matplotlib', 'Plotly'])

    st.subheader("Diagram")
    df = getTelemtryDf(session, selected_drivers, selected_column, area)
    st.dataframe(df)
    try:
        if plot_type == "Matplotlib":
            plotTelemtryMatplotlib(df, selected_drivers)
        elif plot_type == "Plotly":
            plotTelemetryPlotly(df, selected_drivers)
    except:
        st.error('Plot could not be found!')

else:
    st.subheader('Data has not been loaded!')
    st.text('Please visit the main page and select a session')
