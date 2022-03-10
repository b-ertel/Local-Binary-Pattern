from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
from PIL import Image
import numpy as np
import base64
from page.app import app as app
from page.data import *
import plotly.express as px
from util import *




image_transformation = dbc.Card(
    [
        html.H4("Overall Settings", className="card-title"),
        dcc.Upload(id="upload-image", children=html.Div(["Drag and Drop or ", html.A("Select File")]), style = {"borderWidth" : "1px", "borderStyle": "dashed", "borderRadius": "5px", "margin": "10px", "textAlign": "center"},),
        html.Div(
            [
                dbc.Label("Image index"),
                dbc.Input(id="image-index", type="number", value=35), #change this for brodatz-data
            ]
        ),
        html.Div(
            [
                dbc.Label("LBP radius"),
                dbc.Input(id="lbp-radius2", type="number", value=1),
            ]
        ),
        html.Div(
            [
                dbc.Label("LBP: number of points"),
                dbc.Input(id="lbp-number-points2", type="number", value=8),
            ]
        ),

        dbc.Label("LBP: method"),
        dcc.Dropdown(
            id="lbp-method2",
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
    Input("upload-image", "contents")
)
def input_image(value, upload_image):
    if upload_image is not None:
        decoded = base64.b64decode(upload_image.split("base64,")[1])
        image = Image.open(io.BytesIO(decoded))
        image = np.asarray(image)
    if upload_image is None:
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
