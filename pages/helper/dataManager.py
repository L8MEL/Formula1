import fastf1 as f1
import fastf1.core

import pandas as pd
from copy import deepcopy

class DataManager:

    def __init__(self, year, track, event_type):
        # Parameters
        self.year = year
        self.track = track
        self.event_type = event_type
        # Temporary F1 Session
        self.loaded_data = False
        session = self.__getFastF1Session()

        self.resolution = 10
        # Calculated values
        if self.loaded_data:
            self.winner = self.__getWinner(session)
            self.track_weather = self.__calculateTrackWeather(session)
            self.drivers = self.__getDrivers(session)
            self.results = self.__getResults(session)
            self.__telemetry = self.__getTelemetry(session)
            self.__lapData = self.__getLapData(session)

    def __getFastF1Session(self):
        #f1.Cache.set_disabled()
        #f1.Cache.enable_cache('f1_cache')
        try:
            s = f1.get_session(self.year, self.track, self.event_type)
            s.load()
            self.loaded_data = True
        except Exception as e:
            print("An exception occured" + str(e))
            self.loaded_data = False
            return None
        return s

    def __calculateTrackWeather(self, session: f1.core.Session) -> pd.DataFrame:
        df: pd.DataFrame = pd.DataFrame(session.laps.pick_driver(self.__getWinner(session)).get_weather_data())
        return df

    @staticmethod
    def __getWinner(session: f1.core.Session) -> str:
        df = deepcopy(session.results)
        df.sort_values('GridPosition', inplace=True)
        return df.iloc[0].Abbreviation

    @staticmethod
    def __getResults(session: fastf1.core.Session) -> pd.DataFrame:
        df = deepcopy(session.results)
        df.drop(labels=['TeamColor', 'Time'], axis=1,
                inplace=True)
        return df

    @staticmethod
    def __getDrivers(session: fastf1.core) -> list:
        return pd.unique(session.laps['Driver'])

    def __getTelemetry(self, session: fastf1.core.Session) -> dict[str, pd.DataFrame]:
        telemetry = dict()
        for driver in self.drivers:
            telemetry[driver]: pd.DataFrame = pd.DataFrame(session.laps.pick_driver(driver).get_car_data().add_distance())
        return telemetry

    def __getLapData(self, session: fastf1.core.Session) -> dict[str, pd.DataFrame]:
        lapData = dict()
        for driver in self.drivers:
            lapData[driver]: pd.DataFrame = pd.DataFrame(session.laps.pick_driver(driver))
        return lapData

    def __calcAdditionalTelemtryData(self):
        for driver in self.drivers:
            self.__telemetry[driver]['Acceleration'] = 0
            for i in range(len(self.__telemetry[driver].index)):
                self.__telemetry[driver].at[i, 'Acceleration'] = ((self.__telemetry[driver].at[i, 'Speed'] -
                                                                   self.__telemetry[driver].at[i-1, 'Speed']) / 3.6) / \
                                           (self.__telemetry[driver].at[i, 'Time'].total_seconds() -
                                            self.__telemetry[driver].at[i-1, 'Time'].total_seconds())

    def getTelemetryDF_allDriver(self, key: str) -> pd.DataFrame:
        df: pd.DataFrame = pd.DataFrame()
        for driver in self.drivers:
            df[driver] = self.telemetry[driver][key]

        return df

    def getDistanceToLeaderDF(self) -> pd.DataFrame:
        df = self.getTelemetryDF_allDriver('Distance')
        df = df.subtract(df.max(axis=1), axis=0)
        df = df.iloc[lambda x: x.index % self.resolution == 0]
        return df

    def getTelemtryDf_oneLap(self, lap: int) -> pd.DataFrame:
        telemetry = dict()
        for driver in self.drivers:
            #print(driver)
            lap_df = deepcopy(self.lapData[driver])
            #print(list(lap_df['Time']))
            try:
                lapStartTime = lap_df.loc[lap_df['LapNumber'] == lap]['LapStartTime'].to_list()[0]
                lapEndTime = lap_df.loc[lap_df['LapNumber'] == lap]['LapStartTime'].to_list()[0]
            except Exception as e:
                print(e)
                telemetry[driver] = pd.DataFrame()
                continue
            print(lapEndTime)
            lapStartTime = pd.to_timedelta(lapStartTime)
            lapEndTime = pd.to_timedelta(lapEndTime)
            #print(type(lapEndTime))
            tel_df = self.__telemetry[driver]
            tel_df = tel_df.loc[tel_df['Time'] > lapStartTime]
            telemetry[driver] = tel_df.loc[tel_df['Time'] < lapEndTime]

        return telemetry


    @property
    def telemetry(self) -> dict[str, pd.DataFrame]:
        tmp_dict = dict()
        for driver in self.__telemetry.keys():
            tmp_dict[driver] = self.__telemetry[driver].iloc[lambda x: x.index % self.resolution == 0]
        return tmp_dict

    @property
    def lapData(self) -> dict[str, pd.DataFrame]:
        return self.__lapData

    @property
    def trackTemp_mean(self):
        return round(self.track_weather.TrackTemp.mean(), 1)

    @property
    def humidity_mean(self):
        return int(round(self.track_weather.Humidity.mean()))

    @property
    def airTemp_mean(self):
        return round(self.track_weather.AirTemp.mean(), 1)

    @property
    def windSpeed_max(self):
        return round(self.track_weather.WindSpeed.max(), 1)

    @property
    def telemetryColumns(self):
        return self.telemetry[self.winner].columns

    @property
    def lapsDriven(self):
        return self.__lapData[self.winner]['LapNumber'].max()
