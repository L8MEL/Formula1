import fastf1 as f1
import fastf1.core
import pandas as pd
import copy
from pages.helper.helper import *

def calcBoxStop(session: f1.core.Session) -> dict[str: list]:
    all_stops = dict()
    for driver in getDrivers(session):
        stops = list()
        stopped = False
        df: pd.DataFrame = session.laps.pick_driver(driver).get_car_data()
        for row in df.itertuples():
            if row.Speed <105:
                if row.Speed < 1:
                    start = row.Time
                    stopped = True
                if stopped and row.Speed > 0:
                    end = row.Time
                    stopped = False
                    stops.append((end-start).total_seconds())
        all_stops[driver] = stops

    return all_stops






year = 2022
track = 'Melbourne'
event = 'Race'

f1.Cache.enable_cache('f1_cache')
s = f1.get_session(year, track, event)
s.load()

weather = getWeather(s)
print(123)