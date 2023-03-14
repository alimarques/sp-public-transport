import streamlit as st
import numpy as np

from plot_map import plot_stations
from load_data import Loader
from transform_data import Transformer
    
gtfs = Loader()
transform = Transformer(gtfs)
df_stations = transform.transform_data()
df_lines = transform.transform_line_data()

st.title("Metrô de SP")

routes_and_stations = df_stations[['route_id', 'stop_name']].drop_duplicates().reset_index(drop=True)


stations = []
for route in routes_and_stations['route_id'].unique():
    station = st.sidebar.multiselect(
        'Linha ' + route,
        df_stations[df_stations['route_id'] == route]['stop_name'].unique())
    stations += station

stations = np.unique(stations).tolist()

#for route in routes_and_stations['route_id'].unique():
#    df_aux = routes_and_stations[routes_and_stations['route_id'] == route].reset_index(drop=True)
#    st.sidebar.header(route)
#    for s in range(len(df_aux)):
#        label = df_aux['stop_name'][s]
#        select = st.sidebar.checkbox(label=label, value=False, key=label)
#        if select:
#            stations.append(select)

plot_stations(df_stations, stations)