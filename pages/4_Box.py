import streamlit as st
import plotly.express as px
import pandas as pd
from pages.helper.helper import calcBoxStop

data_loaded = False
try:
    session = st.session_state['session']
    data_loaded = True

except Exception as e:
    print(e)
    data_loaded = False

if data_loaded:
    st.title('Boxenstopps')
    st.subheader('Driver Selection')

    selected_drivers = st.selectbox(label="Drivers", options=pd.unique(session.laps['Driver']))

    df = pd.DataFrame(calcBoxStop(session=session))
    df['Size'] = 20
    #df.replace(to_replace=0, value=None, inplace=True)

    def setNone(x):
        if x < 0.1:
            return None
        else:
            return x

    for column in df.columns:
        df[column] = df[column].apply(lambda x: setNone(x))

    fig = px.bar(df, x='Counter', y=selected_drivers, size = 'Size', height=800, width=1600)

    st.plotly_chart(fig)
else:
    st.subheader('Data not loaded')
#st.dataframe(df)