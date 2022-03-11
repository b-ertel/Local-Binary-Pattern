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





@app.callback(
    Output("selected-bins-text", "children"),
    Input('lbp-hist', "selectedData"),
)
def bins_to_text(selected):
    if selected is None:
        return None
    allpoints = selected["points"]
    numbers = [allpoints[i]["x"] for i in range(len(allpoints))]
    return f"Selected: {numbers}"






@app.callback(
    Output("marked-image", "figure"),
    Input("transformed_image", "data"),
    Input('lbp-hist', "selectedData"),

)
def marked_image(json_image, selected):
    x, y = selection_to_mask(selected)
    grey_image = image_from_json(json_image)
    fig = px.imshow(grey_image, binary_string=True)
    fig.add_trace(go.Scatter(x = x, y = y, mode = "markers", marker=dict(color='red', size=5), opacity=0.5 ))
    fig.layout.height = 800
    fig.layout.width = 800
    return fig


def show_lbp_filter(integer_number):
    binary_array = integer_to_binary(integer_number)
    marker = []
    marker_dict = {1:100, 0:0} #flip this if dark = 0 and bright = 1
    P = 8
    #circle
    y = (np.sin(2 * np.pi * np.arange(P, dtype=np.double) / P)).tolist()
    x = (np.cos(2 * np.pi * np.arange(P, dtype=np.double) / P)).tolist()
    for i, val in enumerate(binary_array[::-1]): #reverse it...
        marker.append(marker_dict[val])
    #middle point
    x.append(0)
    y.append(0)
    marker.append(3)

    fig = go.Figure(go.Scatter(mode = "markers", x=x, y=y, marker_symbol = marker))
    fig.update_layout(title = str(integer_number), height = 150, width = 150)
    fig.update_xaxes(visible = False)
    fig.update_yaxes(visible=False)
    fig["layout"].update(margin=dict(l=0, r=5, b=5, t=30))
    return fig


@app.callback(
    Output("all-filters", "children"),
    Input('lbp-hist', "selectedData"),
)
def create_filter_html(selection):
    integer_numbers = selection_to_int_array(selection)
    figures = [show_lbp_filter(i) for i in integer_numbers]
    content = [dbc.Col(dcc.Graph(figure = fig, id=f"filter_{num}")) for fig, num in zip(figures, integer_numbers)]
    content = [dbc.Row(content[i:i+4]) for i in range(len(content)//4+1)]
    return content

filters =   dbc.Row([
                dbc.Col(html.Div(id = "all-filters",
                 style={})),
                     ])