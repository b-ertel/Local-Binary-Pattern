import dash
from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
from skimage.feature import local_binary_pattern
from skimage.color import label2rgb
import dash_bootstrap_components as dbc
from util import *
import base64
import io
from page.app import app as app
from page.input import image_transformation as image_transformation
from page.input import input_image as input_image
from page.data import *
from page.lbp import *
from page.explanation import *



app.layout = dbc.Container(
    [   html.Div(children=[
        html.H1("Local Binary Pattern Visualization"),
        html.H2("on different datasets"),
        html.Hr(),
    ], style={'textAlign': 'center'}),
        #############################INPUT######################################
        dbc.Row(
            [
                html.Div(html.H2("Input and Settings"), style={'textAlign': 'center'}),
                # dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
                dbc.Col(html.Div(children = [html.H3("Original image"),
                    html.Div(children=[dcc.Graph(id="input-image"), ],
                         style={'display': 'inline-block'})], style={'textAlign': 'center'})),
                dbc.Col(image_transformation, md=4),
                dbc.Col(html.Div(children = [html.H3("Transformed image"),
                                             dcc.Store("transformed_image"), dcc.Store("input_image_data"),
                    html.Div(children=[dcc.Graph(id="grey-image")], style={'display': 'inline-block'})], style={'textAlign': 'center'})),
            ],
            align="center",
        ),
        #############################    LBP   ######################################
        html.Hr(),
        dbc.Row([
            html.Div(html.H2("Local Binary Pattern Histogram"), style={'textAlign': 'center'}),
            dbc.Col(lbp_setting, width=3),
            dbc.Col(html.Div(children=[dcc.Graph(id="lbp-hist")],
                             style={'display': 'inline-block'}))
            ]
        ),

        #############################    EXPLANATION    #################################
        html.Hr(),
        dbc.Row([
            html.Div(html.H2("Overlay and Filters"), style={'textAlign': 'center'}),
            html.Div(id ="selected-bins-text", style={'textAlign': 'center'}),
            dbc.Col(  html.Div(children=[dcc.Graph(id="marked-image")],
                 ),
                  ),
            dbc.Col(filters),

            ]
        )
    ],
    fluid=True,
)


server = app.server





if __name__ == '__main__':
    app.run_server(debug=True, port=8051)