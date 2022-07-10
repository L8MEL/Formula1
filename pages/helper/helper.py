import fastf1.core
import pandas as pd
import streamlit as st
import fastf1 as f1
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
