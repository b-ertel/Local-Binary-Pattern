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
    Input('image-index', "value"),
    Input("lbp-radius", "value"),
    Input("lbp-number-points", "value"),
    Input('lbp-hist', "selectedData"),
    Input("lbp-method", "value"),
)
def marked_image(image_index, lbp_radius, lbp_number_points, selected, lbp_method):
    numbers = selection_to_int_array(selected)
    x, y = selection_to_mask(selected)
    image = dataset[image_index][0]
    grey = np.array(to_grey_scale(image, dataset_name))
    lbp = local_binary_pattern(grey, lbp_number_points, lbp_radius, lbp_method)
    edge_labels = numbers
    mask = np.logical_or.reduce([lbp == each for each in edge_labels])
    masky, maskx = np.where(mask)
    overlay = overlay_labels(image, lbp, edge_labels)
    # grey_image = to_grey_scale(image)
    # fig = px.imshow(overlay)
    grey_image = to_grey_scale(image, dataset_name)
    fig = px.imshow(grey_image, binary_string=True)
    fig.add_trace(go.Scatter(x = x, y = y, mode = "markers", marker=dict(color='red', size=5), opacity=0.5 ))
    fig.layout.height = 800
    fig.layout.width = 800
    return fig


def show_lbp_filter(integer_number):
    binary_array = integer_to_binary(integer_number)
    radius = 1
    slices = np.deg2rad(45)
    x = []
    y = []
    color = []
    marker = []
    marker_dict = {1:100, 0:0}
    P = 8
    #circle
    y = (np.sin(2 * np.pi * np.arange(P, dtype=np.double) / P)).tolist()
    x = (np.cos(2 * np.pi * np.arange(P, dtype=np.double) / P)).tolist()
    for i, val in enumerate(binary_array[::-1]): #reverse it...

        # x.append(np.cos(-i*slices+4*slices))
        # y.append(np.sin(-i*slices+4*slices))
        marker.append(marker_dict[val])
        # color.append(str(val))
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
    Output("html-test", "children"),
    Input('lbp-hist', "selectedData"),
)
def create_filter_html(selection):
    integer_numbers = selection_to_int_array(selection)
    integer_number = int(integer_numbers[0])
    figures = [show_lbp_filter(i) for i in integer_numbers]
    content = [dbc.Row([dbc.Col(dcc.Graph(figure = fig, id=f"filter_{num}"))]) for fig, num in zip(figures, integer_numbers)]
    return content

filters =   dbc.Row([
                dbc.Col(html.Div(id = "html-test",
                 style={})),
                     ])