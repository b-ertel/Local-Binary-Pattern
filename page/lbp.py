from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from PIL import Image
import numpy as np
import base64
from page.app import app as app
from page.data import *
import plotly.express as px
from util import *
from skimage.feature import local_binary_pattern
import json


lbp_setting = dbc.Card(
    [
        html.H4("LBP Settings", className="card-title"),
        html.Div(
            [
                dbc.Label("LBP radius"),
                dbc.Input(id="lbp-radius", type="number", value=1),
            ]
        ),
        html.Div(
            [
                dbc.Label("LBP: number of points"),
                dbc.Input(id="lbp-number-points", type="number", value=8),
            ]
        ),

        dbc.Label("LBP: method"),
        dcc.Dropdown(
            id="lbp-method",
            options=[
                {"label": str(i), "value": i} for i in ["default", "ror", "uniform", "nri_uniform"]
            ],
            value="default",
            clearable=False,
        ),
],
    body= True
)




@app.callback(
    Output("lbp-hist", "figure"),
    Input("transformed_image", "data"),
    Input("lbp-radius", "value"),
    Input("lbp-number-points", "value"),
    Input("lbp-method", "value"),
)
def lbp_hist(json_image,lbp_radius, lbp_number_points, lbp_method):
    grey_image = image_from_json(json_image)
    lbp = local_binary_pattern(grey_image, lbp_number_points, lbp_radius, lbp_method).flatten()
    fig = go.Figure(data=[go.Histogram(x=lbp, nbinsx=int(lbp.max()+1))])
    # fig.update_layout(yaxis_range=[0, 4000])
    # fig.update_yaxes(title_text="y-axis in logarithmic scale", type="log")
    fig.layout.height = 450
    fig.layout.width  = 1000
    fig["layout"].update(margin=dict(l=0, r=0, b=0, t=0))
    return fig