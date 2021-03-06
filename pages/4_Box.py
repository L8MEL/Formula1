import streamlit as st
import plotly.express as px
import pandas as pd
from pages.helper.helper import *
from pages.helper.sets import session_selection, sideBarLayout

session = loadSession()
sideBarLayout()
st.title('Boxenstopps')
if session is not None and st.session_state['event_type'] == 'Race':

    st.subheader('Driver Selection')

    selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']))

    df = pd.DataFrame(calcBoxStop(session=session))
    df['Size'] = 20
    #df.replace(to_replace=0, value=None, inplace=True)

    def setNone(x):
        if type(x) == str:
            return x
        if x < 0.1:
            return None
        else:
            return x

    for column in df.columns:
        df[column] = df[column].apply(lambda x: setNone(x))

    df.dropna(inplace=True, axis=0, how='all')

    fig = px.bar(df, x='Counter', y=selected_drivers, barmode='group')

    st.plotly_chart(fig)
elif not st.session_state['event_type'] == 'Race':
    st.warning('This analysis can only be displayed for the race!')
else:
    st.subheader('Data not loaded')
#st.dataframe(df)