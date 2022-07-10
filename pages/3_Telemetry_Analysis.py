import fastf1.core
import fastf1 as f1
import fastf1.plotting
import pandas as pd
import numpy as np
import streamlit as st
from pages.helper.helper import *
import matplotlib.pyplot as plt

from pages.helper.sets import *

try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data laoded. \n Please got to main")

if data_loaded:
    session: fastf1.core.Session = st.session_state['session']
    st.subheader("Results")

    # Driver and Data Selector
    st.subheader("Detailled Analysis")
    selected_drivers = st.multiselect(label="Drivers", options=pd.unique(session.laps['Driver']),
                                      default=pd.unique(session.laps['Driver'])[0])

    selected_column = st.selectbox(label="Data",
                                   options=session.laps.pick_driver(selected_drivers[0]).get_car_data().columns)

    col1, col2 = st.columns(2)
    area = col1.radio(label="Select Area", options=['Fastest', 'All'])
    plot_type = col2.radio(label="Select Plot", options=['Matplotlib', 'Interactive'])

    st.subheader("Diagram")
    f1.plotting.setup_mpl()
    if area == 'Fastest':
        df = session.laps.pick_driver(selected_drivers[0]).pick_fastest().get_car_data().add_distance()[
            'Distance'].to_frame()
    else:
        df = session.laps.pick_driver(selected_drivers[0]).get_car_data().add_distance()['Distance'].to_frame()

    fig, ax = plt.subplots(figsize=(16, 8))

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
        # pd.concat(df, y.to_frame())

        print(type(x))
        ax.plot(x, y, linewidth=0.5)
    ax.legend(selected_drivers)
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    plt.xticks(rotation=45)
    if plot_type == "Matplotlib":
        st.pyplot(fig)

    else:
        try:
            df.set_index('Distance', inplace=True)
            st.line_chart(df, height=400)
        except:
            st.text("Plotting Error")

        print(session.laps.pick_drivers(selected_drivers).pick_fastest().
              get_pos_data().sort_values('Date').drop(columns=['SessionTime', 'Time', 'Date', 'Status', 'Source']).
              set_index('X'))
    st.subheader('Map View')
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
        print(selected_drivers)

        st.pyplot(fig)
    except:
        st.text("Error Positon Data not found!")
else:
    st.subheader('Data has not been loaded!')
    st.text('Please visit the main page and select a session')
