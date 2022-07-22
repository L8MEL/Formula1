import requests
import pandas as pd


class RaceInformationManager:

    def __init__(self, year):
        self.year = year
        self.fetch_data()
        self.races, self.race_info = self.getRaces()

    def fetch_data(self):
        r = requests.get('https://ergast.com/api/f1/%s.json?limit=1000000' % self.year)
        self.data = r.json()['MRData']

    def getRaces(self):
        races = list()
        df = pd.DataFrame()
        for race in self.data['RaceTable']['Races']:
            races.append(race['raceName'])
            tmp_dict = dict()
            for key in race.keys():
                if key == 'Circuit': continue
                tmp_dict[key] = [race[key]]

            for key in race['Circuit'].keys():
                if key == 'Location': continue
                tmp_dict[key] = [race['Circuit'][key]]

            for key in race['Circuit']['Location']:
                tmp_dict[key] = [race['Circuit']['Location'][key]]

            df = pd.concat((df, pd.DataFrame.from_dict(tmp_dict)), ignore_index=True)
        return races, df
