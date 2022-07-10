import fastf1 as f1

year = 2022
track = 'Melbourne'
event = 'Race'

f1.Cache.enable_cache('f1_cache')
s = f1.get_session(year, track, event)
s.load()
print("End")