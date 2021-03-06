import pandas as pd
import pydeck
import altair as alt
import folium

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]

mydf = pd.DataFrame({
    'name': ['Constanta, Romania', 'Turin, Italy', 'Madrid, Spain', 'Copenhagen', 'Berlin'],
    'lat': [45.1598, 45.0703, 40.4168, 55.6761, 52.5200],
    'long': [28.6348, 7.6869, -3.7038, 12.5683, 13.40]
    })

descriptions = ['I was born here!',
               'I grew up and earned my degrees here.',
               'I studied psychology here for one year.',
               'I worked at the IT university.',
               'Home since July 2020.']

mydf['descr'] = descriptions

def get_map():

    layer = pydeck.Layer(
    "HeatmapLayer",
    mydf,
    opacity=0.9,
    get_position=["long", "lat"],
    get_fill_color=[180, 0, 200, 140],
    color_range = COLOR_BREWER_BLUE_SCALE,
    get_weight=1)

    view_state = pydeck.ViewState(
    longitude=11.5820,
    latitude=48.1351,
    zoom=2,
    min_zoom=2,
    max_zoom=2,
    pitch=0,
    bearing=0)

    r = pydeck.Deck(layers=[layer], initial_view_state=view_state, map_style='light')

    return r

def get_altair_map():
    map_ = alt.Chart(mydf).mark_circle().encode(
    longitude='long',
    latitude='lat',
    size=alt.value(50),
    tooltip='name'
    ).project(
    type= 'mercator',
    scale= 350,                          # Magnify
    center= [20,50],                     # [lon, lat]
    clipExtent= [[0, 0], [400, 300]],    # [[left, top], [right, bottom]]
    ).properties(
    width=500,
    height=400
    )

    return map_


def get_folium_map():
    # center on Liberty Bell
    z = 4
    m = folium.Map(location=[48.1351, 11.5820], zoom_start=z, min_zoom=z, max_zoom=z, zoom_control=False)

    for i, row in mydf.iterrows():
        folium.Marker([row['lat'], row['long']], tooltip=row['name'] + '. ' + row['descr'],).add_to(m)

    return m
