from typing import List, Any

import streamlit as st

from pages.helper.sets import sideBarLayout

sideBarLayout()

st.title('Results')
st.write('The result of the session is displayed below')

st.table(st.session_state['session'].results.drop(
    columns=['Time', 'Q1', 'Q2', 'Q3', 'TeamColor', 'FirstName', 'LastName']))
