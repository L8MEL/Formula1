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

st.subheader("Results")
session = loadSession()

if session is not None:
    sideBarLayout()
    session: fastf1.core.Session = loadSession()


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
    #st.dataframe(df)
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
