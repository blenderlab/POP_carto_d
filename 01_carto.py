# bibliotheque ppoue executer des requetes web :
import requests
'''
fichier de configuration (config.py) enregistré à côté de ce fichier. il contient l'API etc.
Plus pratique pour se refiler du code... mais tout le monde doit utiliser la même convention

apikey=''
lang='fr'
name='Thomas HOCEDEZ'
'''
import config as conf

baseurl='http://api.openweathermap.org/data/2.5/weather?appid='+conf.apikey + "&units=metric"


def get_locations():
    geocode=[] # geocode = tableau des listes de coord
    lonlat=open('lonlat.txt', 'r') # ouverture du fichier
    for line in lonlat:
        lon, lat=line.split(',') # on découpe la ligne à la ","
        coord={} # coord est une liste vide
        coord["lat"]=lon.strip() #on ajoute un objet "lon"
        coord["lon"]=lat.strip()#on ajoute un objet "lat"
        geocode.append(coord) # on ajoute la coord au tableau (à la fin)
    return geocode #on renvoie notre joli tableau

def display_location(l,titre):
    '''
    petite fonction qui affiche proprement une liste de type 'coord'
    on reçoit une liste au format :
        {'lon':xxxx, 'lat':yyyy}
    et un titre 'titre', pour faire joli.

    pour chaque objet (nommé 'item') de la liste 'l'
        'item' est donc un élément de la liste, au format :
            'lat':xxxx
        on l'imprime (donc son nom : 'lon', 'lat', ...)
        avec à côté sa valeur (l['lon'], l['lat'] ...)
    '''
    print(titre)
    for item in l:
        print(item, " = ", l[item])

def get_weather(c):
    '''
    on reçoit une liste au format :
        {'lon':xxxx, 'lat':yyyy}
    on la nomme 'c'
    On recrée l'url de recherche avec ces coordonnées
    On execute la requete à l'aide de l'objet "requests"
    les résultats seront stockés dans un objet JSON nommé "weather"
    Dans notre liste 'c', on crée un objet 'temp', dans lequel on vient enregistre la température de "Weather"

    notre liste est donc au format :
        {'lon':xxxx, 'lat':yyyy, 'temp':zzzz}
    On termine en renvoyant tout notre 'c' (qui est notre liste de base, augmentée de la température)
    '''

    url = baseurl + "&lon="+c["lon"] + "&lat="+c['lat']
    weather=requests.get(url).json()
    c["temp"]=weather['main']['temp']
    return c


def main():
    '''
    on génère notre tableau de coordonnées à partir du fichier :
    ce tableau se nomme "locations"
    ueions", on traite chaque ligne, qu'on nomme "location"
    chacune est donc une liste au format :
            {'lon':xxxx, 'lat':yyyy}
    on i notre 'location' par la nouvelle, enrichie par la température.

    et on l'affiche (la location)
    '''
    nbligne=0
    locations = get_locations()
    for location in locations :
        location = get_weather(location)
        nbligne=nbligne+1
        sep = "=== LIGNE %d ==="  % nbligne
        display_location(location,sep)

'''
petite convention pour faire un code CLEAN :
notre programme principal, est maintenant une fonction : main()
La ligne ci-dessous, est typique de Python, elle signifie que si ce programme est le principal, alors on execute la fonction main().
ce fonctionnement évite d'avoir du code perdu un peu partout.
bref, c'est mieux.
'''
if __name__ == "__main__":
    main()