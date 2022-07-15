import pandas as pd
import plotly.express as px
import streamlit as st
import datetime


import fastf1 as f1
import fastf1.core

def getSpeedTrapDf(session: f1.core.Session, selected_drivers: list, speedTrap: str) -> pd.DataFrame:
    index_translate = {'Sector1Time': 9, 'SpeedI1': 13, 'SpeedI2': 14, 'SpeedFL': 15, 'SpeedST': 16}
    df = pd.DataFrame()
    max_laps = 0
    for driver in selected_drivers:
        driver_speeds = list()
        lap_counter = 0
        for lap in session.laps.pick_driver(driver).iterlaps():
            lap_counter += 1
            #print(lap[1][13])
            if 'Time' in speedTrap:
                driver_speeds.append(lap[1][index_translate[speedTrap]] + session.date.normalize())
            else:
                driver_speeds.append(lap[1][index_translate[speedTrap]])
        max_laps = max(lap_counter, max_laps)

        df[driver] = driver_speeds
    df['Laps'] = list(range(1, max_laps+1))
    return df

def plotDf(df: pd.DataFrame, selected_drivers: list, speedTrap: str) -> None:
    col1, col2, col3 = st.columns(3)
    width = col1.number_input(label='Width', min_value=100, max_value=2000, value=1200)
    height = col2.number_input(label='Height', min_value=100, max_value=2000, value=800)
    marker_size = col3.number_input(label='Marker Size', min_value=1, max_value=30, value=5)
    type = st.radio(label='Type', options=['Scatter', 'Line'])
    if type =='Scatter':
        fig = px.scatter(df, x='Laps', y=selected_drivers, width=width, height=height)
        fig.update_traces(marker_size=marker_size, marker_symbol="circle-dot", marker_line_width=0.1*marker_size)
        fig.update_layout(legend_title="Driver")
    elif type == 'Line':
        fig = px.line(df, x='Laps', y=selected_drivers, width=width, height=height)

    # if 'Time' in speedTrap:
    #     print('Contains Time')
    #     fig.update_layout(xaxis_tickformat='%H-%M-%S')
    st.plotly_chart(fig)


