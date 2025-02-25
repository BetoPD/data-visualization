# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from helpers import load_housing_data

# Incorporate data
housing = load_housing_data()
numeric_columns = housing.select_dtypes(include=['number']).columns.tolist()

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]

map_styles = ["basic",
"carto-darkmatter",
"carto-darkmatter-nolabels",
"carto-positron",
"carto-positron-nolabels",
"carto-voyager",
"carto-voyager-nolabels",
"dark",
"light",
"open-street-map",
"outdoors",
"satellite",
"satellite-streets",
"streets"]


app = Dash('__name__', external_stylesheets=external_stylesheets, title='California Housing')


# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('California Housing Prices', className="text-primary text-center fs-3 mt-3")
    ]),

    dbc.Row([
        dbc.Col([
        html.Div([
            dash_table.DataTable(
                data=housing.to_dict('records'), 
                page_size=12, 
                style_table={'overflowX': 'auto'}, 
                style_cell={'textAlign': 'center'}),], 
            className="p-3 bg-light border rounded-3 shadow-sm")  # Background + Border + Shadow
        ], width=6),

        dbc.Col([
            html.Div([
                dcc.Graph(figure={}, id='histogram-graph'),            
                html.Div([
                    html.Button("Next Histogram", id="next-btn", n_clicks=0, className="btn btn-primary"),
                ], 
            className="d-flex justify-content-center mt-3")], 
        className="p-3 bg-light border rounded-3 shadow-sm")], 
    width=6)], 
className='m-auto d-flex justify-content-center mt-5'),
    
    dbc.Row([
        dbc.Col([
        html.Div([
              dcc.Graph(figure={}, id='scatter-graph'),
              html.Div([
                    html.Button("Next Map", id="next-map", n_clicks=0, className="btn btn-primary")], className="d-flex justify-content-center mt-3"),
              ], className="p-3 bg-light border rounded-3 shadow-sm"),
        ], width=12),

    ], className='m-auto d-flex justify-content-center mt-5')

])


# Add controls to build the interaction
@callback(
    Output('histogram-graph', 'figure'),
    Input('next-btn', 'n_clicks')
)
def update_graph(n_clicks):
    col_chosen = numeric_columns[n_clicks % len(numeric_columns)]  # Ciclar entre columnas
    fig = px.histogram(housing, x=col_chosen)
    return fig


@callback(
    Output('scatter-graph', 'figure'),
    Input('next-map', 'n_clicks')
)
def update_map(n_clicks):
    return px.scatter_map(
                  data_frame=housing,
                    lat=housing['latitude'],
                    lon=housing['longitude'],
                    zoom=3,
                    color=housing['median_house_value'],
                    size=housing['population'] / 100,
                    height=600,
                    map_style=map_styles[n_clicks % len(map_styles)],
                    title=f'Map style: {map_styles[n_clicks % len(map_styles)]}'
              )

# Run the app
if __name__ == '__main__':
    app.run(debug=True, dev_tools_hot_reload=True)



