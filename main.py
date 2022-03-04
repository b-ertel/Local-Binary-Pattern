from dataset import *
import torchvision.transforms as transforms
from dash import Dash, dcc, html, Input, Output, no_update
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
from skimage.feature import local_binary_pattern
from skimage.color import label2rgb


# dataset = ETHDataset(transform=transforms.Compose([
#                                # transforms.Resize(image_size),
#                                transforms.CenterCrop([256,256]),
#                                transforms.ToTensor(),
#                            ]))

dataset = BrodatzDataset(transform=transforms.Compose([
                               # transforms.Resize(image_size),
                               transforms.CenterCrop([256,256]),
                               transforms.ToTensor(),
                           ]))
dataset_name = "brodatz"


test = dataset.__getitem__(0)[0]

dataset.__getitem__(0)
dataset.get_path(10)
dataset.get_attribute_name(0)

app = Dash("Dashboard for LBP")



def to_grey_scale(image, dataset_name):
    if dataset_name == "brodatz":
        grey_image = (image.squeeze(2)*255).astype(np.uint8)
    else:
        grey_image = Image.fromarray((image * 255).astype(np.uint8)).convert("L")
    return grey_image





def overlay_labels(image, lbp, labels):
    mask = np.logical_or.reduce([lbp == each for each in labels])
    image = to_grey_scale(image, dataset_name)
    return label2rgb(mask, image=image, bg_label=0, alpha=0.2)



app.layout = html.Div(
    className="container",
    children=[
        html.Div(children=[
            html.H3(children='Visualizing Local Binary Pattern'),
            html.H6(children='on ETH synthesizability dataset', style={'marginTop': '-15px', 'marginBottom': '30px'})
        ], style={'textAlign': 'center'}),
        dcc.Input(
            id='image_number',
            type='number',
            value=5
        ),
        html.Div(children = [dcc.Graph(id ="input-image")],
                 style={'display': 'inline-block'}),
        html.Div(children=[dcc.Graph(id="grey-image")],
                 style={'display': 'inline-block'}),
        html.Div(children=[dcc.Graph(id="lbp-hist")],
                 style={'display': 'inline-block'}),
        html.Div(id='bins-text'),
        html.Div(children=[dcc.Graph(id="marked-image")],
                 style={}),
    ],
)


@app.callback(
    Output("input-image", "figure"),
    Input('image_number', "value"),
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
    Input('image_number', "value"),
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
    Input('image_number', "value"),
)
def lbp_hist(value):
    image = dataset[value][0]
    n_points = 8
    radius = 3
    grey_image = to_grey_scale(image, dataset_name)
    lbp = local_binary_pattern(grey_image, n_points, radius, "nri_uniform").flatten()
    # hist1, _ = np.histogram(lbp, np.arange(2 ** n_points + 1), density=True)
    fig = go.Figure(data=[go.Histogram(x=lbp, nbinsx=2**n_points)])
    fig.layout.height = 450
    return fig


@app.callback(
    Output("marked-image", "figure"),
    Input('image_number', "value"),
    Input('lbp-hist', "selectedData"),
)
def marked_image(value, selected):
    if selected is not None:
        allpoints = selected["points"]
        numbers = [allpoints[i]["x"] for i in range(len(allpoints))]
    if selected is None:
        numbers = [1,2,3,4,5]
    image = dataset[value][0]
    n_points = 8
    radius = 3
    grey = np.array(to_grey_scale(image, dataset_name))
    lbp = local_binary_pattern(grey, n_points, radius, "nri_uniform")
    edge_labels = numbers
    overlay = overlay_labels(image, lbp, edge_labels)
    fig = px.imshow(overlay)
    fig.layout.height = 800
    fig.layout.width = 800
    return fig


@app.callback(
    Output("bins-text", "children"),
    Input('lbp-hist', "selectedData"),
)
def bins_to_text(selected):
    if selected is None:
        return None
    allpoints = selected["points"]
    numbers = [allpoints[i]["x"] for i in range(len(allpoints))]
    return f"selected: {numbers}"




if __name__ == '__main__':
    app.run_server(debug=True)
    print("test")