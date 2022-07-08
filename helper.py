import fastf1.core
import streamlit as st
import fastf1 as f1


@st.cache(allow_output_mutation=True)
def getSession(track, year, event):
    #f1.Cache.set_disabled()
    f1.Cache.enable_cache('f1_cache')
    s = f1.get_session(year, track, event)
    s.load()
    return s


def getResults(session: fastf1.core.Session):
    session.load()
    df = session.results
    df.drop(labels=['TeamColor', 'FirstName', 'LastName', 'FullName', 'Q1', 'Q2', 'Q3', 'Time'], axis=1,
                   inplace=True)
    print(df)
    return df