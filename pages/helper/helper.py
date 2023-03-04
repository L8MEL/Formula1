import fastf1.core
import pandas as pd
import streamlit as st
import fastf1 as f1
from copy import deepcopy
import numpy as np
import os




def getSession(track: str, year: int, event: str) -> None:
    # f1.Cache.set_disabled()
    with st.spinner('Data is loading...'):
        st.session_state['track'] = track
        st.session_state['year'] = year
        st.session_state['event_type'] = event


        f1.Cache.enable_cache('f1_cache')
        try:
            s = f1.get_session(year, track, event)
            if s is not None:
                s.load()
                st.session_state['session'] = s
        except:
            st.error('Data not available')
        return

def calcBoxStop(session: f1.core.Session):
    all_stops = dict()
    all_stops['Counter'] = list( ['Start', *list(range(1, 10))])

    for driver in getDrivers(session):
        stops = np.zeros(10)
        counter = 0
        stopped = False
        df: pd.DataFrame = session.laps.pick_driver(driver).get_car_data()
        for row in df.itertuples():
            if row.Speed < 1:
                try:
                    print(row.Status)
                except:
                    print("No Status")
                start = row.Time.total_seconds()
                stopped = True
            if stopped and row.Speed > 0:
                end = row.Time.total_seconds()
                stopped = False
                stops[counter] = (round((end-start), 2))
                counter += 1
        all_stops[driver] = stops

    return all_stops

def getWeather(session: f1.core.Session):
    return session.laps.pick_driver(getWinner(session)).get_weather_data()

def getWinner(session: f1.core.Session):
    df = session.results
    df.sort_values('GridPosition', inplace=True)
    return df.iloc[0].Abbreviation

def getDrivers(session: fastf1.core):
    return pd.unique(session.laps['Driver'])


def loadSession() -> tuple:
    try:
        session = st.session_state['session']
        return session
    except:
        st.error('Failed to load session data. Please reload at main page!')

    return None

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total