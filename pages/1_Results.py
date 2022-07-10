from typing import List, Any

import streamlit as st
from pages.helper.helper import getResults

try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data laoded. \n Please got to main")

if data_loaded:
    session = st.session_state['session']
    df = getResults(session)
    st.title("Results")
    columns: list[str] = st.multiselect(label='Select Information', options=df.columns, default=df.columns[0])

    st.table(df[columns])
