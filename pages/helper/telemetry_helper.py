import fastf1 as f1
import fastf1.core
import fastf1.plotting
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache
def getResults(session: fastf1.core.Session) -> pd.DataFrame:
    df = pd.DataFrame(session.results)
    df.to_numpy()
    df.drop(labels=['TeamColor', 'Time'], axis=1,
            inplace=True)
    return df

def plotMapMatplotlib(session: fastf1.core.Session, selected_drivers: list, area: str):


    fig, ax = plt.subplots(figsize=(16, 8))
    try:
        for driver in selected_drivers:
            if area == 'Fastest':
                x = session.laps.pick_driver(driver).pick_fastest().telemetry['X']
                y = session.laps.pick_driver(driver).pick_fastest().telemetry['Y']
            else:
                x = session.laps.pick_driver(driver).telemetry['X']
                y = session.laps.pick_driver(driver).telemetry['Y']

            points = np.array([x, y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            ax.plot(x, y, linewidth=2)

        ax.set_facecolor('#0E1117')
        fig.patch.set_facecolor('#0E1117')
        ax.axis('off')
        ax.legend(selected_drivers)
        st.pyplot(fig)
    except:
        print("Failes plotting")


def plotTelemtryMatplotlib(df: pd.DataFrame, selected_drivers: list) -> None:
    f1.plotting.setup_mpl()
    fig, ax = plt.subplots(figsize=(16, 8))
    for driver in selected_drivers:
        ax.plot(df['Distance'], df[driver], linewidth=0.5)
    ax.legend(selected_drivers)
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plotTelemetryPlotly(df: pd.DataFrame, selected_drivers: list) -> None:
    col1, col2 = st.columns(2)
    width = col1.number_input(label='Width', min_value=100, max_value=2000, value=1200)
    height = col2.number_input(label='Height', min_value=100, max_value=2000, value=800)
    fig = px.line(df, x='Distance', y=selected_drivers, width=width, height=height)
    st.plotly_chart(fig)

def getTelemtryDf(session: fastf1.core.Session, selected_drivers: list, selected_column,  area: str) -> pd.DataFrame:
    df = pd.DataFrame()
    data_points = 0
    for driver in selected_drivers:
        data_points = max(data_points, len(session.laps.pick_driver(driver).pick_fastest().get_car_data().index))
    df['Distance'] = [0 for x in range(data_points)]
    for driver in selected_drivers:
        if area == 'Fastest':
            x = session.laps.pick_driver(driver).pick_fastest().get_car_data().add_distance()['Distance']
            y = session.laps.pick_driver(driver).pick_fastest().get_car_data()[selected_column]
        else:
            x = session.laps.pick_driver(driver).get_car_data().add_distance()['Distance']
            y = session.laps.pick_driver(driver).get_car_data()[selected_column]
        if max(x) > df['Distance'].max():
            df['Distance'] = x
        df[driver] = y
        df.dropna(how='any', inplace=True)
    return df