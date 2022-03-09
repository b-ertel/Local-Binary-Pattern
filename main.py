from dataset import *
import torchvision.transforms as transforms
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


##############CONFIGS, DATA, ETC #####################################
# dataset = BrodatzDataset(transform=transforms.Compose([
#                                # transforms.Resize(image_size),
#                                transforms.CenterCrop([256,256]),
#                                transforms.ToTensor(),
#                            ]))
# dataset_name = "brodatz"

dataset = ETHDataset(transform=transforms.Compose([
                               # transforms.Resize(image_size),
                               transforms.CenterCrop([256,256]),
                               transforms.ToTensor(),
                           ]))

dataset_name = "eth"


########################################################################


app = dash.Dash(
    external_stylesheets=[dbc.themes.COSMO]
)



controls = dbc.Card(
    [
        html.H4("Overall Settings", className="card-title"),
        html.Div(
            [
                dbc.Label("Image index"),
                dbc.Input(id="image-index", type="number", value=35), #change this for brodatz-data
            ]
        ),
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
                {"label": str(i), "value": i} for i in ["default", "ror", "uniform", "nri_uniform", "var"]
            ],
            value="default",
            clearable=False,
        ),
],
    body= True
)



@app.callback(
    Output("input-image", "figure"),
    Input('image-index', "value"),
)
def input_image(value):
    image = dataset[value][0]
    if image.shape[2] == 1:
        image = image.squeeze(2)
        fig = px.imshow(image, binary_string=True)
    else:
        fig = px.imshow(image)
    fig.layout.height = 400
    fig.layout.width = 400
    return fig

@app.callback(
    Output("grey-image", "figure"),
    Input('image-index', "value"),
)
def grey_image(value):
    image = dataset[value][0]
    grey_image = to_grey_scale(image, dataset_name)
    fig = px.imshow(grey_image, binary_string=True)
    fig.layout.height = 400
    fig.layout.width = 400
    return fig


@app.callback(
    Output("lbp-hist", "figure"),
    Input('image-index', "value"),
    Input("lbp-radius", "value"),
    Input("lbp-number-points", "value"),
    Input("lbp-method", "value"),
)
def lbp_hist(image_index, lbp_radius, lbp_number_points, lbp_method):
    image = dataset[image_index][0]
    grey_image = to_grey_scale(image, dataset_name)
    lbp = local_binary_pattern(grey_image, lbp_number_points, lbp_radius, lbp_method).flatten()
    # hist1, _ = np.histogram(lbp, np.arange(2 ** n_points + 1), density=True)
    fig = go.Figure(data=[go.Histogram(x=lbp, nbinsx=int(lbp.max()+1))])
    fig.layout.height = 450
    return fig


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

@app.callback(
    Output("filters", "figure"),
    Input('lbp-hist', "selectedData"),
)
def show_lbp_filter(selection):
    integer_numbers = selection_to_int_array(selection)
    integer_number = int(integer_numbers[0])
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
    fig.update_layout(title = str(integer_number), height = 300, width = 300)
    fig.update_xaxes(visible = False)
    fig.update_yaxes(visible=False)
    return fig

filters = html.Div(children=[dcc.Graph(id="filters")],
                 style={})

app.layout = dbc.Container(
    [   html.Div(children=[
        html.H1("Local Binary Pattern Visualization"),
        html.H2("on different datasets"),
        html.Hr(),
    ], style={'textAlign': 'center'}),
        dbc.Row(
            [
                html.Div(html.H2("Input and Settings"), style={'textAlign': 'center'}),
                dbc.Col(controls, md=4),
                # dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
                dbc.Col(html.Div(children = [html.H3("Input image"),
                    html.Div(children=[dcc.Graph(id="input-image")],
                         style={'display': 'inline-block'})], style={'textAlign': 'center'})),
                dbc.Col(html.Div(children = [html.H3("Grey image"),
                    html.Div(children=[dcc.Graph(id="grey-image")], style={'display': 'inline-block'})], style={'textAlign': 'center'})),
            ],
            align="center",
        ),
        dbc.Row([
            html.Div(html.H2("Local Binary Pattern Histogram"), style={'textAlign': 'center'}),
            html.Div(children=[dcc.Graph(id="lbp-hist")],
                     style={'display': 'inline-block'}),
            ]
        ),
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








if __name__ == '__main__':
    app.run_server(debug=True, port=8051)