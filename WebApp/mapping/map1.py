import folium
from folium.vector_layers import CircleMarker
import pandas as pd

# Load in volcano data via pd
data = pd.read_csv('WebApp/mapping/Volcanoes.txt')

# Create separate lists for latitudes and longitudes
lats = list(data['LAT'])    
lons = list(data['LON'])
elev = list(data['ELEV'])
locs = list(data['LOCATION'])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Starting point for Map
map = folium.Map(location=[lats[0], lons[0]], zoom_start=6, tiles="Stamen Terrain")

# Create layer for all markers
fg = folium.FeatureGroup(name="My Map")

html = """<h4>Volcano information:</h4>
Height: %s m <br/>
Location: %s
"""

# Iterate through lists to place new markers for each volcano
for lt, ln, el, lc in zip(lats, lons, elev, locs):
    iframe = folium.IFrame(html=html % (str(el), lc), width=200, height=200)
    
    fg.add_child(folium.CircleMarker(location=[lt,ln], popup=folium.Popup(iframe), radius=6, color='grey', fill_color=color_producer(el), fill_opacity=0.8))


fg.add_child(folium.GeoJson(data=open('WebApp/mapping/world.json', 'r', encoding='utf=8=sig').read()))

map.add_child(fg)

map.save("Map1.html")
