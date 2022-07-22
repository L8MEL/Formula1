import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import fastf1 as f1
import fastf1.core
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pages.helper.sets import *

index_dict = {'Time': 0, 'DriverNumber': 1, 'LapTime': 2, 'LapNumber': 3, 'Stint': 4, 'PitOutTime': 5, 'PitInTime': 6,
              'Sector1Time': 7, 'Sector2Time': 8, 'Sector3Time': 9, 'Sector1SessionTime': 10, 'Sector2SessionTime': 11,
              'Sector3SessionTime': 12, 'SpeedI1': 13, 'SpeedI2': 14, 'SpeedFL': 15, 'SpeedST': 15,
              'IsPersonalBest': 16, 'Compound': 18, 'TyreLife': 19, 'FreshTyre': 20, 'LapStartTime': 20, 'Team': 21,
              'Driver': 22, 'TrackStatus': 23, 'IsAccurate': 24, 'LapStartDate': 25}


def getSpeedTrapDf(session: f1.core.Session, selected_drivers: list, speedTrap: str) -> pd.DataFrame:
    global index_dict
    df = pd.DataFrame()
    for driver in selected_drivers:
        lap_counter = 0
        for lap in session.laps.pick_driver(driver).iterlaps():
            lap = lap[1]
            lap_data = dict()
            lap_counter += 1
            lap_data['Driver'] = [driver]
            lap_data['Lap'] = [lap[index_dict['LapNumber']]]
            if 'Time' in speedTrap:
                lap_data['Value'] = [lap[index_dict[speedTrap]] + session.date.normalize()]
            else:
                lap_data['Value'] = [lap[index_dict[speedTrap]]]

            df = pd.concat((df, pd.DataFrame.from_dict(lap_data)), axis=0)

    return df


def getStints(session: f1.core.Session, selected_drivers: list):
    # df = pd.DataFrame({'index': 0, 'Driver': 'XXX', 'Counter': 0, 'Lap': 0, 'Tire': 'XXX', 'Stint_Distance': 0})
    global index_dict
    df = pd.DataFrame()

    index = 1
    for driver in selected_drivers:
        for lap in session.laps.pick_driver(driver).iterlaps():
            print(lap)
            print('Started')
            pit_Stop = dict()
            lap = lap[1]
            print('Calc....')
            pit_Stop['index'] = [index]
            pit_Stop['Driver'] = [driver]
            pit_Stop['Lap'] = lap[index_dict['LapNumber']]
            pit_Stop['Tire'] = lap[index_dict['Compound']]
            pit_Stop['Stint_Distance'] = lap[index_dict['Stint']]

            print('Concat..')
            tmp_df = pd.DataFrame.from_dict(pit_Stop)
            df = pd.concat((df, tmp_df), axis=0)
            index += 1
    print(df)

    return df


# Plots
def plotDf(df: pd.DataFrame, width: int, height: int, marker_size: int, type: str) -> None:
    if type == 'Scatter':
        fig = px.scatter(df, x='Lap', y='Value', color='Driver', width=width, height=height, marginal_y="violin")
        fig.update_traces(marker_size=marker_size, marker_symbol="circle", marker_line_width=0.1 * marker_size)
        fig.update_layout(legend_title="Driver")
        #fig.update_xaxes(range=[0, df.Lap.max()])
    elif type == 'Line':
        fig = px.line(df, x='Lap', y='Value', color='Driver', width=width, height=height)
        fig.update_layout(legend_title="Driver")
        fig.update_traces(line_width=marker_size)
        #fig.update_xaxes(range=[0, df.Lap.max()])

    st.plotly_chart(fig)


def plotStints(df: pd.DataFrame, width: int, height: int, marker_size: int, type: str, max_laps: int) -> None:
    fig = px.scatter(df, x='Lap', y='Driver', color='Tire', width=width, height=height * 0.3,
                     color_discrete_map={
                         "SOFT": "red",
                         "MEDIUM": "yellow",
                         "HARD": "White"})
    fig.update_xaxes(range=[0, max_laps])
    fig.update_traces(marker_size=marker_size)
    st.plotly_chart(fig)


def plotAll(stint_df: pd.DataFrame, lap_df: pd.DataFrame, width: int, height: int, marker_size: int, type: str,
            selected_driver: list):
    fig = make_subplots(rows=2, cols=1)
    for driver in selected_driver:
        fig.add_trace(go.Scatter(x=lap_df.loc(lap_df['Driver'] == driver)['Lap'],
                                 y=lap_df.loc(lap_df['Driver'] == driver)['LapTime']), row=1, col=1)

        fig.add_trace(go.Scatter(x=lap_df.loc(lap_df['Driver'] == driver)['Tire'],
                                 y=lap_df.loc(lap_df['Driver'] == driver)['Tire']), row=2, col=1)
