import requests
import config 
import smopy 
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
from matplotlib.mlab import griddata

# using the current weather API : 
baseurl='http://api.openweathermap.org/data/2.5/weather?appid='+config.apikey + "&units=metric"

def get_locations(filename):
    #-- Read the data.
    # I'm going to use `pandas` to read in and work with your data, mostly due to
    # the text site names. Using pandas is optional, however.
    data = pd.read_csv(filename, delim_whitespace=False)
    return data 

def print_dict(l,titre):
    # Same as 01_carto.py
    print("==== %s ====" % titre)
    for item in l:
        print(item, " = ", l[item])

def get_area(locations):
    lat_min=locations.lat.min()
    lon_min=locations.lon.min()
    lat_max=locations.lat.max()
    lon_max=locations.lon.min()
    # adding some border  (10%):
    o_lat = ((lat_max - lat_min)/100)*10
    o_lon = ((lon_max - lon_min)/100)*10
    lat_min=lat_min-o_lat
    lat_max=lat_max+o_lat
    lon_min=lon_min-o_lat
    lon_max=lon_max+o_lat
    # finally , return directly a list
    return {'lat_min':lat_min, 'lat_max':lat_max, 'lon_min':lon_min,'lon_max':lon_max}

def get_weather(c):
    # Same as 01_carto.py
    url = baseurl + "&lon="+c.lon + "&lat="+c.lat
    weather=requests.get(url).json()
    c.temp=weather['main']['temp']    
    return c

def get_map(locations):
    area = get_area(locations)
    map = smopy.Map( (area['lat_min'],area['lon_min'],area['lat_max'],area['lon_max']) , z=8)
    # Create a figure with the map : 
    ax = map.show_mpl(figsize=(8,8))

    
    #-- Now let's grid your data.
    # First we'll make a regular grid to interpolate onto. This is equivalent to
    # your call to `mgrid`, but it's broken down a bit to make it easier to
    # understand. The "30j" in mgrid refers to 30 rows or columns.
    numcols, numrows = 30, 30
    xi = np.linspace(locations.lon.min(), locations.lon.max(), numcols)
    yi = np.linspace(locations.lat.min(), locations.lat.max(), numrows)
    xi, yi = np.meshgrid(xi, yi)
    
    #-- Interpolate at the points in xi, yi
    # "griddata" expects "raw" numpy arrays, so we'll pass in
    # locations.x.values instead of just the pandas series data.x
    x, y, z = locations.lon.values, locations.lat.values, locations.temp.values
    zi = griddata(x, y, z, xi, yi)
    
    #-- Display the results
    fig, ax = plt.subplots()
    im = ax.contourf(xi, yi, zi)
    ax.scatter(data.Lon, locations.lat, c=locations.temp, s=100,vmin=zi.min(), vmax=zi.max())
    fig.colorbar(im)
    
    plt.show()
    
def main():
    #1 - get locations from file :
    locations = get_locations('lonlat.txt')
    print(locations)

    #2 - add weather for each point :
    for location in locations :
        location = get_weather(location)


    #3 display locations (print) :
    nbligne=0
    for location in locations :
        nbligne=nbligne+1
        sep = "LIGNE %d"  % nbligne
        print_dict(location,sep)
        
 
    #4 - get the map (according to boundaries)
    map = get_map(locations)
    
    # NOW, we have all the data we need, no more API Request !




if __name__ == "__main__":
    main()