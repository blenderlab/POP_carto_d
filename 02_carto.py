import requests
import config 

baseurl='http://api.openweathermap.org/data/2.5/weather?appid='+config.apikey + "&units=metric"

def get_locations(filename):
    # Same as 01_carto.py
    geocode=[] # geocode = tableau des listes de coord
    lonlat=open(filename, 'r') # ouverture du fichier
    for line in lonlat:
        lon, lat=line.split(',') # on découpe la ligne à la ","
        coord={} # coord est une liste vide
        coord["lat"]=lon.strip() #on ajoute un objet "lon"
        coord["lon"]=lat.strip()#on ajoute un objet "lat"
        geocode.append(coord) # on ajoute la coord au tableau (à la fin)
    return geocode #on renvoie notre joli tableau

def print_dict(l,titre):
    # Same as 01_carto.py
    print("==== %s ====" % titre)
    for item in l:
        print(item, " = ", l[item])

def get_area(locations):
    # get area boundaries.
    # initialising min/max with first record #0
    lat_min=lat_max=float(locations[0]['lat'])
    lon_min=lon_max=float(locations[0]['lon'])
    # let's check each record :
    for location in locations :
        lat_min=min(lat_min,float(location['lat']))
        lat_max=max(lat_max,float(location['lat']))
        lon_min=min(lon_min,float(location['lon']))
        lon_max=max(lon_max,float(location['lon']))
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
    url = baseurl + "&lon="+c["lon"] + "&lat="+c['lat']
    weather=requests.get(url).json()
    print(weather)
    c["temp"]=weather['main']['temp']
    return c


def main():
    #1 - get locations from file :
    locations = get_locations('lonlat.txt')


    #2 - add weather for each point :
    for location in locations :
        location = get_weather(location)

    #3 - get area boundary  :
    area = get_area(locations)
    print_dict(area,"AREA")

    #4 - get the map (according to boundaries)

    # NOW, we have all the data we need, no more API Request !

    #4 display locations (print) :
    nbligne=0
    for location in locations :
        nbligne=nbligne+1
        sep = "LIGNE %d"  % nbligne
        print_dict(location,sep)



if __name__ == "__main__":
    main()