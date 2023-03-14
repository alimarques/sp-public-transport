import streamlit as st
import geopandas as gpd
import leafmap
from shapely.geometry import Point, LineString

@st.cache_resource
class Transformer:
    def __init__(self, _gtfs):
        self.gtfs = _gtfs
        self.gtfs.routes['route_color'] = self.transform_colors_hex(self.gtfs.routes['route_color'])

    def transform_colors_hex(self, colors):
        hex_colors = colors.apply(lambda x: '#' + x)
        return hex_colors

    def transform_data(self):
        df = self.gtfs.stop_times.merge(self.gtfs.trips, on='trip_id', how='left')[['trip_id', 'stop_id', 'route_id', 'shape_id', 'direction_id']].drop_duplicates().reset_index(drop=True)
        df = df.merge(self.gtfs.stops, on='stop_id', how='left')
        df = df.merge(self.gtfs.routes, on='route_id', how='left')

        df = df[df['route_type'] != 3]  # Remove bus trips
        df = df[df['direction_id'] == 0]    # Remove duplication caused by direction
        df = df.rename(columns={'stop_lat':'lat', 'stop_lon':'lon'})

        df['geometry'] = df.apply(lambda x: Point((float(x['lon']), float(x['lat']))), axis=1)
        df = gpd.GeoDataFrame(df, geometry='geometry')
        return df

    def transform_line_data(self):
        df = self.gtfs.trips.merge(self.gtfs.routes, on='route_id', how='left')
        df = df.merge(self.gtfs.shapes, on='shape_id', how='left')
        df = df[df['route_type'] != 3]  # Remove bus trips
        df = df[df['direction_id'] == 0]    # Remove duplication caused by direction
        df = df.rename(columns={'shape_pt_lat':'lat', 'shape_pt_lon':'lon'})

        df['geometry'] = df.apply(lambda x: Point((float(x['lon']), float(x['lat']))), axis=1)
        df = gpd.GeoDataFrame(df, geometry='geometry')
        df = df.groupby(['route_id','route_color'])['geometry'].apply(lambda x: LineString(x.tolist()))
        df = gpd.GeoDataFrame(df, geometry='geometry')
        return df