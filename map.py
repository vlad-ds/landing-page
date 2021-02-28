import pandas as pd
import pydeck

COLOR_BREWER_BLUE_SCALE = [
    [240, 249, 232],
    [204, 235, 197],
    [168, 221, 181],
    [123, 204, 196],
    [67, 162, 202],
    [8, 104, 172],
]


def get_map():
    mydf = pd.DataFrame({
    'name': ['Constanta', 'Turin', 'Madrid', 'Jyvaskyla', 'Copenhagen', 'Berlin'],
    'lat': [45.1598, 45.0703, 40.4168, 62.2426, 55.6761, 52.5200],
    'long': [28.6348, 7.6869, -3.7038, 25.7473, 12.5683, 13.40]
    })

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
    min_zoom=5,
    max_zoom=15,
    pitch=0,
    bearing=0)

    r = pydeck.Deck(layers=[layer], initial_view_state=view_state, map_style='light')

    return r




