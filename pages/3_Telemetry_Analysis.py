import fastf1.core
import fastf1 as f1
import fastf1.plotting
import pandas as pd
import numpy as np
import streamlit as st
from pages.helper.helper import *
import matplotlib.pyplot as plt

from pages.helper.sets import *
from pages.helper.sets import session_selection, sideBarLayout

try:
    session = st.session_state['session']
    data_loaded = True
except:
    data_loaded = False
    st.subheader("No data laoded. \n Please got to main")

if "data_manager" in st.session_state:
    manager: DataManager = st.session_state['data_manager']
    if manager.loaded_data:
        sideBarLayout()

        st.subheader("Results")

        # Driver and Data Selector
        st.subheader("Detailled Analysis")
        selected_drivers = st.multiselect(label="Drivers", options=pd.unique(manager.drivers),
                                          default=manager.winner)

        selected_column = st.selectbox(label="Data",
                                       options=manager.telemetryColumns)

        col1, col2 = st.columns(2)
        area = col1.radio(label="Select Area", options=['One', 'All'])
        plot_type = col2.radio(label="Select Plot", options=['Matplotlib', 'Interactive'])

        st.subheader("Diagram")
        f1.plotting.setup_mpl()

        if area == 'One':
            lap = st.slider(label="Lap Selector", min_value=0, max_value=manager.lapsDriven, value=0)
            df = manager.getTelemtryDf_oneLap(lap)
        else:
            df = manager.getTelemetryDF_allDriver(selected_column)


        if plot_type == "Matplotlib":

            fig, ax = plt.subplots(figsize=(16, 8))

                df[driver] = y
                # pd.concat(df, y.to_frame())

                print(type(x))
                ax.plot(x, y, linewidth=0.5)


            ax.legend(selected_drivers)
            ax.set_facecolor('#0E1117')
            fig.patch.set_facecolor('#0E1117')
            plt.xticks(rotation=45)
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

        except:
            st.text("Error Positon Data not found!")
else:
    st.subheader('Data has not been loaded!')
    st.text('Please visit the main page and select a session')
