import requests
import config 
import smopy 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

# using the current weather API : 
baseurl='http://api.openweathermap.org/data/2.5/weather?appid='+config.apikey + "&units=metric"

def get_locations(filename):
    data = pd.read_csv(filename, delim_whitespace=False)
    return data 

def get_area(locations):
    lat_min=locations.lat.min()
    lon_min=locations.lon.min()
    lat_max=locations.lat.max()
    lon_max=locations.lon.max()
    # adding some border  (10%):
    o_lat = ((lat_max - lat_min)/100)*10
    o_lon = ((lon_max - lon_min)/100)*10
    lat_min=lat_min-o_lat
    lat_max=lat_max+o_lat
    lon_min=lon_min-o_lat
    lon_max=lon_max+o_lat
    # finally , return directly a list
    return {'lat_min':lat_min, 'lat_max':lat_max, 'lon_min':lon_min,'lon_max':lon_max}

def get_weather(r):
    # Same as 01_carto.py
    url = baseurl + ("&lon={}&lat={}").format(r['lon'],r['lat'])
    weather=requests.get(url).json()
    return weather['main']['temp']

def get_map(locations):
    area = get_area(locations)
    map = smopy.Map( (area['lat_min'],area['lon_min'],area['lat_max'],area['lon_max']) , z=8)
    # Create a figure with the map : 
    fig, ax = plt.subplots()
    ax = map.show_mpl(figsize=(8,8))
    for index, row in locations.iterrows():
        row['x'],row['y'] = map.to_pixels(float(row['lat']),float(row['lon']))
        ax.plot(row['x'],row['y'], 'sg', ms=5)
        ax.annotate(row['temp'],xy=(row['x'],row['y']),xytext=(row['x']+5,row['y']+5))
    ax.scatter(locations.x, locations.y, c=locations.temp, s=100,vmin=locations.temp.min(), vmax=locations.temp.max())
    
    plt.show()
    
def main():
    #1 - get locations from file :
    locations = get_locations('lonlat.txt')
    locations['temp']=0
    locations['x']=locations['y']=0
    #2 - add weather for each point :
    x, y= locations.lon.values, locations.lat.values
    for index, row in locations.iterrows():
        locations.loc[index,'temp'] = get_weather(row)
    #4 - get the map (according to boundaries)
    print(locations)    
    map = get_map(locations)
    # NOW, we have all the data we need, no more API Request !




if __name__ == "__main__":
    main()