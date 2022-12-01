import streamlit as st
import scipy
import requests
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk
from geopy.geocoders import Nominatim
from geopy.distance import great_circle as GRC
from shapely.geometry import Point
import json
import plotly.figure_factory as ff
import matplotlib.pyplot as plt


END_NOMINATIM =  "https://nominatim.openstreetmap.org/"
APPARTMENT = "Appartement"
HOUSE = "Maison"

df = pd.read_csv("immo_lyon17_22Epuré.csv", low_memory = False)

### Configuration
st.set_page_config(
    page_title="Ventefacile",
    page_icon="🦠 ",
    layout="wide"
)

### App
st.title('Valeur de mon bien')
st.markdown("👋 Bonjour et bienvenue sur cette application qui vous servira à évaluer votre bien immobilier sur la ville de LYON")
st.caption("Les données utilisées proviennent de la période entre le 01 Juillet 2017 et le 30 Juin 2022")
st.subheader('veuillez entrer les différentes caractéristiques de votre bien')

col1, col2, col3, col4 = st.columns(4)
with col1 :
    option = st.selectbox(
    'Dans quel arrondissement se situe votre bien ?',
    ('1er', '2e', '3e','4e','5e','6e','7e','8e','9e'))
    st.write("Votre arrondissement est le : ",option)
with col2 :
    number = st.number_input('Entrez le numéro de votre adresse',value = 45, step = 1 )
    st.write("le numéro de l'adresse est : ", number)
with col3 :
    name = st.text_input("Entrez le nom de la rue", value = "rue de la bourse")
    st.write("le nom de la rue est : ",name)
with col4 :
    post = st.number_input("Entrez le code postale de votre bien", value = 69002, min_value = 69000, max_value = 69009, step = 1)
    st.write("le code postale est :",post)

col5, col6, col7 = st.columns(3)
with col5 :
    apoumaiz = st.selectbox(
    'Votre bien est il un Appartement ou une Maison ?', 
    (APPARTMENT, HOUSE))
    if apoumaiz == APPARTMENT :
        st.write("Il s'agit d'un", apoumaiz)
    else :
        st.write("Il s'agit d'une", apoumaiz)
with col6 :
    nombre = st.number_input("Combien de pièce votre bien possède-t-il ?", value = 1, min_value = 1, max_value = 21, step = 1)
    if nombre == 1 :
        st.write("Votre bien possède ", nombre, "pièce")
    else :
        st.write("Votre bien possède ", nombre, "pièces")
with col7 : 
    surf = st.number_input("Quelle est la surface habitable ?", value = 0, step = 1)
    st.write("La surface habitable est de ", surf, "m²")

adress = str(number) + " " + name

#locator = Nominatim(user_agent="galli.vincent.ts6@live.fr")
locations = requests.get(END_NOMINATIM+"search", params={'city':"LYON", "street" : adress, "postalcode" : post, "country" : "FRANCE", "format":"json"} ).json() 

for location in locations :
    if location["osm_type"] == "node":
        place = location
    else :
        print("L'adresse mentionnée comporte une faute, veuillez rentrer la bone adresse.")

point1 = (float(place["lat"]), float(place["lon"]))

list_gps = []
for longitude, latitude in zip(df.longitude, df.latitude):
    list_gps.append((latitude, longitude))

df['tuple_gps'] = list_gps

my_dist = []
for coordinate in df.tuple_gps:
            #print(count)
            point2 = coordinate
            result = GRC(point1,point2).m
            result = round(result,2)
            my_dist.append(result)
df["distance"] = my_dist

df_map = df.filter(items = ["distance", "valeur_fonciere","latitude", "longitude","type_local"])
if apoumaiz == APPARTMENT :
    mask_appart = df_map['type_local'] == APPARTMENT
    df_map = df_map[mask_appart]
else :
    mask_house = df_map["type_local"] == HOUSE
    df_map = df_map[mask_house]

df_map = df_map.sort_values(by = ["distance"], ascending = True)
df_map = df_map[:10]
print(df_map)

fig = px.scatter_mapbox(df_map, lat="latitude", lon="longitude", mapbox_style = 'carto-positron', color="type_local", size="valeur_fonciere", 
                center={"lat":float(place["lat"]),"lon":float(place["lon"])},
                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=12)

plot_spot = st.empty() # holding the spot for the graph

#send the plotly chart to it's spot "in the line" 
with plot_spot:
   st.plotly_chart(fig, use_container_width=True)
