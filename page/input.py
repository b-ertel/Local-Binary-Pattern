from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc
from PIL import Image
import numpy as np
import base64
from page.app import app as app
from page.data import *
import plotly.express as px
from util import *
import json
import io




image_transformation = dbc.Card(
    [
        html.H4("Import an image", className="card-title"),
        dbc.Label("(default dataset will be gone until you refresh the page)"),
        dcc.Upload(id="upload-image", children=html.Div(["Drag and Drop or ", html.A("Select File")]), style = {"borderWidth" : "1px", "borderStyle": "dashed", "borderRadius": "5px", "margin": "10px", "textAlign": "center"},),
        html.Div(
            [
                dbc.Label("Change to see other image from the Brodatz dataset"),
                dbc.Input(id="image-index", type="number", value=1), #change this for brodatz-data
            ]
        ),
        dbc.Label("Zoom into the image"),
        html.Div([
            dcc.Slider(1, 4, 0.25,
                       value=1,
                       id='zoom-factor'
                       ),
            # html.Div(id='zoom-container', children = "Zoom-factor")
        ]),
        dbc.Label("Shift in X"),
        html.Div([
            dcc.Slider(0, 256, 1, value=0, marks=None, id = "zoom-x",
    tooltip={"placement": "bottom", "always_visible": False}),
            # html.Div(id='zoom-x-container', children="Shift in X")
        ]),
        dbc.Label("Shift in Y"),
        html.Div([
            dcc.Slider(0, 256, 1, value=0, marks=None, id = "zoom-y",
    tooltip={"placement": "bottom", "always_visible": False}),
            # html.Div(id='zoom-y-container', children= "Shift in Y")
        ]),
        dbc.Label("Scale the image down by the factor"),
        html.Div([
            dcc.Slider(1, 4, 0.25,
                       value=1,
                       id='scale-factor'
                       ),
            # html.Div(id='scale-container', children="Scale")
        ]),
],
    body= True
)



@app.callback(
    Output("input-image", "figure"),
    Output("input_image_data", "data"),
    Input('image-index', "value"),
    Input("upload-image", "contents")
)
def input_image(value, upload_image):
    if upload_image is not None:
        decoded = base64.b64decode(upload_image.split("base64,")[1])
        image = Image.open(io.BytesIO(decoded))
        small_side = image.size[0] if image.size[0] < image.size[1] else image.size[1]
        left = (image.size[0]-small_side)//2
        top = (image.size[1]-small_side)//2
        image = image.crop((left,top,left + small_side, top + small_side))
        image = image.resize((400,400))
    if upload_image is None:
        image = dataset[value][0]
    if image.mode != "RGB":
        image = image.convert("RGB")
    fig = px.imshow(image)
    fig.layout.height = 400
    fig.layout.width = 400
    fig["layout"].update(margin=dict(l=0, r=5, b=5, t=30))
    return fig, image_to_json(image)



@app.callback(
    Output("grey-image", "figure"),
    Output("transformed_image", "data"),
    Input("input_image_data", "data"),
    Input('zoom-factor', "value"),
    Input('zoom-x', "value"),
    Input('zoom-y', "value"),
    Input('scale-factor', "value"),
)
def grey_image(input_image, zoom_factor, zoom_x, zoom_y, scale_factor):
    image = image_from_json(input_image)
    if image.mode != "L":
        image = image.convert("L")

    #zoom

    w, h = image.size
    image = image.crop((zoom_x , zoom_y,zoom_x + w//zoom_factor, zoom_y + h//zoom_factor))

    #scale
    w, h = image.size
    image = image.resize((int(w//scale_factor), int(h//scale_factor)))

    fig = px.imshow(image, binary_string=True)
    fig.layout.height = 400
    fig.layout.width = 400
    fig["layout"].update(margin=dict(l=0, r=5, b=5, t=30))

    return fig, image_to_json(image)
