import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import shapely.geometry
import numpy as np

color_scale = [
    [0.0, '#ff3d0d'],
    [1.0, '#0dff62']
]

def plot_lines(df_line):
    lats = []
    lons = []
    names = []
    colors = []
    df_line = df_line.reset_index()
    for feature, name, color in zip(df_line.geometry, df_line.route_id, df_line.route_color):
        if isinstance(feature, shapely.geometry.linestring.LineString):
            linestrings = [feature]
        elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
            linestrings = feature.geoms
        else:
            continue
        for linestring in linestrings:
            x, y = linestring.xy
            lats = np.append(lats, y)
            lons = np.append(lons, x)
            names = np.append(names, [name]*len(y))
            colors = np.append(colors, [color]*len(y))
            lats = np.append(lats, None)
            lons = np.append(lons, None)
            names = np.append(names, None)
            colors = np.append(colors, None)

    fig = px.line_mapbox(lat=lats, lon=lons, hover_name=names, color=colors)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig)


def plot_stations(df, stations):
    df['Visitou'] = df['stop_name'].apply(lambda x: 1.0 if x in stations else 0.0)

    fig = go.Figure(go.Scattermapbox(
        lat=df['lat'],
        lon=df['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color=df['Visitou'],
            colorscale=color_scale
        ),
        text=df['stop_name']
    ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            bearing=0,
            center=dict(
                lat=-23.475,
                lon=-46.584
            ),
            pitch=0,
            zoom=8.9
            ),
        margin={"r":0,"t":0,"l":0,"b":0})

    st.plotly_chart(fig)