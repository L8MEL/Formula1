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


if "data_manager" in st.session_state:
    manager: DataManager = st.session_state['data_manager']
    if manager.loaded_data:
        sideBarLayout()
        st.title('Position')
        st.text('The following diagram shows the Distance to the leader of the race.')

        selected_drivers = st.multiselect(label='Driver selector', options=manager.drivers,
                                          default=manager.drivers[0])

        counter = 0
        st.subheader("Mean Speed")
        columns = st.columns(len(selected_drivers))
        for column in columns:
            column.metric(label=selected_drivers[counter],
                          value=str(round(manager.telemetry[selected_drivers[counter]]['Speed'].mean(), 2)) + ' km/h')
            counter += 1

        st.subheader('Diagram')
        st.line_chart(manager.getDistanceToLeaderDF()[selected_drivers])


