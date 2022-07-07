import streamlit as st
import fastf1 as f1
import fastf1.plotting
import pandas as pd
import datetime
import plotly.express as px
import matplotlib.pyplot as plt

print("Star")
# Setup
f1.Cache.enable_cache('cache/')
st.set_page_config(layout='wide')


grandPrix = ['Melbourne', 'Singapore', 'Spielberg', 'Spa', 'Barcelona', 'Silverstone']


st.title('F1 Race Analysis')
st.subheader("Select Event")
selected_track = st.selectbox(label="Drivers", options=grandPrix)
selected_year = st.selectbox(label="Year", options=list(range(2000, 2023, 1)))
selected_session = st.selectbox(label="Session", options=['FP1', 'FP2', 'FP3', 'Qualifying', 'Race'])

# Load Session
session = f1.get_session(selected_year, selected_track, selected_session)
session.load()
data = session.laps.sort_values('Driver')
drivers = pd.unique(session.laps['Driver'])

selected_drivers = st.multiselect(label="Drivers", options=drivers, default=drivers[0])
selected_column = st.selectbox(label="Data", options=session.laps.pick_driver(selected_drivers[0]).get_car_data().columns)

col1, col2 = st.columns(2)
area = col1.radio(label="Select Area", options=['All', 'Fastest'])
plot_type = col2.radio(label="Select Plot", options=['Matplotlib', 'Interactive'])

st.subheader("Diagram")
f1.plotting.setup_mpl()
if area == 'Fastest':
    df = session.laps.pick_driver(selected_drivers[0]).pick_fastest().get_car_data().add_distance()['Distance'].to_frame()
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
    #pd.concat(df, y.to_frame())

    print(type(x))
    ax.plot(x, y, linewidth=0.5)

plt.xticks(rotation=45)
if plot_type == "Matplotlib":
    st.pyplot(fig)

else:
    try:
        df.set_index('Distance', inplace=True)
        st.line_chart(df, height= 400)
    except:
        st.text("Plotting Error")

print('Done')


