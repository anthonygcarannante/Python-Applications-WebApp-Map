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
map = folium.Map(location=[lats[0], lons[0]], zoom_start=6, tiles="Stamen Toner")

# Create layer for all markers
fg_pop = folium.FeatureGroup(name="Population")
fg_vol = folium.FeatureGroup(name="Volcanoes")

html = """<h4>Volcano information:</h4>
Height: %s m <br/>
Location: %s
"""

# Add country borders to the map as a layer 
fg_pop.add_child(folium.GeoJson(data=open('WebApp/mapping/world.json', 'r', encoding='utf=8=sig').read(), style_function=lambda x: {'fillColor':'blue' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# Iterate through lists to place new markers for each volcano
for lt, ln, el, lc in zip(lats, lons, elev, locs):
    iframe = folium.IFrame(html=html % (str(el), lc), width=200, height=200)
    
    fg_vol.add_child(folium.CircleMarker(location=[lt,ln], popup=folium.Popup(iframe), radius=6, color='grey', fill_color=color_producer(el), fill_opacity=0.8))

# Add layers to the map
map.add_child(fg_pop)
map.add_child(fg_vol)

map.add_child(folium.LayerControl())

# Save to HTML file
map.save("Map1.html")
