import pandas as pd
import streamlit as st

from params import visited_stations

@st.cache_resource
class Loader:
    def __init__(self):
        self.load_visited_stations()
        self.load_gtfs_data()

    def load_visited_stations(self):
        df = pd.DataFrame({'stop_name': visited_stations})
        df['visitou'] = 1
        self.visited_stations = df

    def load_gtfs_data(self):
        self.frequencies = pd.read_csv('gtfs/frequencies.txt')
        self.routes = pd.read_csv('gtfs/routes.txt')[['route_id', 'route_long_name', 'route_type', 'route_color']]
        self.shapes = pd.read_csv('gtfs/shapes.txt')
        self.stop_times = pd.read_csv('gtfs/stop_times.txt')
        self.stops = pd.read_csv('gtfs/stops.txt')
        self.trips = pd.read_csv('gtfs/trips.txt')