import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
from PIL import Image
import altair as alt
import pydeck as pdk
from api_key import mapbox_key

st.image('https://www.swisscancerscreening.ch/typo3conf/ext/mr_swiss_cancer_screening/Resources/Public/Images/Logo2.png',width = 180)

st.title('Analyse des données de participation au dépistage du cancer du sein')

st.subheader('20 années de données de participation de 1999 à 2019')


@st.cache
def load_data(path,DATE_COLUMN = None):
    data = pd.read_csv(path)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    if DATE_COLUMN is not None:
    	data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

path = "./Data/giracs_input.csv"

data = load_data(path)
patients = data[['numerodossier','medecin','autremedecin','mammoanterieure','atf','mammo','rappel']].groupby('numerodossier').sum(min_count = 1)


st.text('Number of people in the dataset: %s' % len(data.numerodossier.unique()))
st.text('Number of people having done a breast cancer screening (mammography): %s' %len(patients[patients.mammo > 0]))

age_group = data.groupby('groupeage').sum()/data.groupby('groupeage').count()
age_group['Age group'] = age_group.index
age_group['mammo'] = age_group['mammo']
st.write(data.head(100))
# a = alt.Chart(age_group,width = 800).mark_bar().encode(
#   x=alt.X('mammo:Q', axis=alt.Axis(format='%', title='Participation')),
#   y=alt.Y('Age group:N', axis=alt.Axis(title='Age group')),
#   color='Age group:N'
# )
# st.altair_chart(a)
n_cat = data.drop('geometry',axis = 1).nunique()
n_cat = n_cat[n_cat < 60].index.sort_values()
group_col = st.sidebar.selectbox("Group by", n_cat, 0) #Add a select box to choose an ATC among the filtered ones
group = data.groupby(group_col).sum()/data.groupby(group_col).count()
group = group.reset_index().sort_values('mammo')
y_var = group_col + ":N"
# st.write(data.head(100))
a = alt.Chart(group,width = 800).mark_bar().encode(
  x=alt.X('mammo:Q',axis=alt.Axis(format='%', title='Participation')),
  y=alt.Y(y_var, axis=alt.Axis(title=group_col))
)
st.altair_chart(a)

buildings_ge = pd.read_pickle('./Data/buildings_ge.pkl')

annee = st.slider('Année', 1999, 2019, 2018)

filtered_data = data[data.year_invit <= annee]
if st.sidebar.checkbox('Show participants only',key = 'Participants'):
	filtered_data = filtered_data[filtered_data.mammo == 1]
filtered_data = filtered_data[['longitude','latitude']]
LAND_COVER  = [[[-74.0, 40.7], [-74.02, 40.7], [-74.02, 40.72], [-74.0, 40.72]]]
material = {'ambient': 0.5,
	'diffuse': 0.6,
	'shininess': 40,
	'specularColor': [60, 64, 70]}
layer = pdk.Layer(
	'GridLayer',
	filtered_data,
	get_position=['longitude', 'latitude'],
	auto_highlight=True,
	cell_size = 800,
	elevation_scale=50,
	pickable=True,
	elevation_range=[0, 300],
	extruded=True,                 
	coverage=1,
	on_hover = 'count')
scatter = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    filtered_data,
    get_position=['longitude', 'latitude'],
    auto_highlight=True,
    get_radius=30,          # Radius is given in meters
    get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
    pickable=True)
polygon = pdk.Layer(
    'PolygonLayer',
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon='-',
    get_fill_color=[180, 0, 0, 0],
    pickable=True
)
# Set the viewport location
view_state = pdk.ViewState(
    longitude=6.14909,
    latitude=46.193,
    zoom=10,
    min_zoom=3,
    max_zoom=30,
    pitch=45,
    bearing=-25)
layers = [scatter,polygon]
if st.sidebar.checkbox('Show buildings blueprint',key = 'Buildings'):
	buildings = pdk.Layer(
        'PolygonLayer',
        buildings_ge,
        extruded = True,
        wireframe = False,
        opacity =  0.5,
        get_polygon = 'polygon',
        get_elevation = 'elevation',
        get_fill_color = [74, 80, 87],
        material = material,
        pickable=True
      )
	layers.append(buildings)
if st.sidebar.checkbox('Show rid heatmap',key = 'Heatmap'):
	layers.append(layer)
r = pdk.Deck(layers=layers, initial_view_state=view_state,mapbox_key = mapbox_key())
st.pydeck_chart(r)
r.to_html('giracs.html')