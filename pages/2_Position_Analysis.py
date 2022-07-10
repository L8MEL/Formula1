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
    for driver in drivers:
        df[driver] = session.laps.pick_driver(driver).get_car_data().add_distance()['Distance']


    df = df.subtract(df.max(axis=1), axis=0)
    df = df.iloc[lambda x: x.index % 10 == 0]
    return df


try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data laoded. \n Please got to main")

if data_loaded:
    st.title('Position')
    st.text('the following diagram shows the Distance to the leader of the race.')
    st.subheader('Diagram')
    data = loadDataFrame()
    selected_drivers = st.multiselect(label='Driver selector', options=data.columns, default=data.columns[0])
    st.line_chart(data[selected_drivers])
