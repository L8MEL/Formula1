import fastf1.core
import pandas as pd
import streamlit as st
import fastf1 as f1
import fastf1.core
from copy import deepcopy
import numpy as np


def getSession(track: str, year: int, event: str) -> None:
    # f1.Cache.set_disabled()
    with st.spinner('Data is loading...'):

        f1.Cache.enable_cache('f1_cache')
        s = f1.get_session(year, track, event)
        if s is not None:
            s.load()
            st.session_state['session'] = s
            st.session_state['data_loaded_successful'] = True

        st.session_state['data_loaded_successful'] = False
        return

@st.cache
def getResults(session: fastf1.core.Session) -> pd.DataFrame:

    session.load()
    df = deepcopy(session.results)
    df.to_numpy()
    df.drop(labels=['TeamColor', 'Time'], axis=1,
            inplace=True)
    return df

def getDrivers(session: fastf1.core):
    return pd.unique(session.laps['Driver'])

def calcBoxStop(session: f1.core.Session) -> dict[str: list]:
    all_stops = dict()
    all_stops['Counter'] = list(range(1, 11))
    for driver in getDrivers(session):
        stops = np.empty(10)
        counter = 0
        stopped = False
        df: pd.DataFrame = session.laps.pick_driver(driver).get_car_data()
        for row in df.itertuples():
            if row.Speed <105:
                if row.Speed < 1:
                    start = row.Time
                    stopped = True
                if stopped and row.Speed > 0:
                    end = row.Time
                    stopped = False
                    stops[counter] = (round((end-start).total_seconds(), 2))
                    counter += 1
        all_stops[driver] = stops

    return all_stops