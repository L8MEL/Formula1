import pandas as pd
import numpy as np
from pages.helper.helper import *
from pages.helper.sets import *
import matplotlib.pyplot as plt
import streamlit as st
import fastf1.core
import fastf1 as f1


def loadDataFrame() -> pd.DataFrame:
    session = st.session_state['session']
    df = pd.DataFrame()
    drivers = pd.unique(session.laps['Driver'])
    speeds = dict()
    for driver in drivers:
        df[driver] = session.laps.pick_driver(driver).get_car_data().add_distance()['Distance']
        speeds[driver] = session.laps.pick_driver(driver).get_car_data().Speed.mean()


    df = df.subtract(df.max(axis=1), axis=0)
    df = df.iloc[lambda x: x.index % 10 == 0]
    return df, speeds


try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data laoded. \n Please got to main")

if data_loaded:
    st.title('Position')
    st.text('The following diagram shows the Distance to the leader of the race.')
    st.subheader('Diagram')
    data, speeds = loadDataFrame()
    selected_drivers = st.multiselect(label='Driver selector', options=data.columns, default=data.columns[0])
    columns = st.columns(len(selected_drivers))
    print(type(columns))
    counter = 0
    for column in columns:
        column.metric(label=selected_drivers[counter], value=str(round(speeds[selected_drivers[counter]], 2)) + ' km/h')
        counter += 1
    st.line_chart(data[selected_drivers])
