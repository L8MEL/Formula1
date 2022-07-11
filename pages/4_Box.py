import streamlit as st
import plotly.express as px
import pandas as pd

from pages.helper.helper import calcBoxStop
session = st.session_state['session']
st.title('Boxenstopps')
st.subheader('Driver Selection')

selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']),
                                  default=pd.unique(session.laps['Driver'])[0])

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

fig = px.scatter(df, x='Counter', y=selected_drivers, size = 'Size', height=800, width=1600)

st.plotly_chart(fig)
#st.dataframe(df)