from typing import Tuple, Any, Dict

import pandas as pd
import numpy as np
from pages.helper.helper import *
from pages.helper.sets import *
import matplotlib.pyplot as plt
import streamlit as st
import fastf1.core
import fastf1 as f1
import copy
from pages.helper.sets import session_selection, sideBarLayout


def loadDataFrame() -> tuple[pd.DataFrame, dict[str, float]]:
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

def calculatePositions(df) -> pd.DataFrame:
    positions = pd.DataFrame(columns=df.columns)
    df = copy.deepcopy(df)
    df.fillna(value=-100000000, inplace=True)

    for position in range(1, len(df.columns)+1):
        max_index = list(df.idxmax(axis="columns"))
        for n in range(0, len(max_index)):
            positions.at[n*10, max_index[n]] = position
            df.at[n*10, max_index[n]] = -1000000000

    return positions

try:
    session = st.session_state['session']
    data_loaded = True

except:
    data_loaded = False
    st.subheader("No data loaded. \n Please got to main")

if data_loaded:
    sideBarLayout()
    st.title('Position')
    st.text('The following diagram shows the Distance to the leader of the race.')
    st.subheader('Diagram')
    data, speeds = loadDataFrame()
    selected_drivers = st.multiselect(label='Driver selector', options=data.columns, default=data.columns[0])
    columns = st.columns(len(selected_drivers))

    counter = 0
    st.subheader("Mean Speed")
    for column in columns:
        column.metric(label=selected_drivers[counter], value=str(round(speeds[selected_drivers[counter]], 2)) + ' km/h')
        counter += 1
    st.subheader()
    st.line_chart([selected_drivers])

