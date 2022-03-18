from PIL import Image
import numpy as np
from skimage.color import label2rgb
import json

def image_to_json(image):
    return json.dumps((np.array(image)).tolist())

def image_from_json(json_image):
    return Image.fromarray(np.array(json.loads(json_image), dtype='uint8'))

def to_grey_scale(image, dataset_name):
    """converts image to greyscale"""
    if dataset_name == "brodatz":
        grey_image = (image.squeeze(2)*255).astype(np.uint8)
    else:
        grey_image = Image.fromarray((image * 255).astype(np.uint8)).convert("L")
    return grey_image


def selection_to_int_array(selected):
    if selected is not None:
        allpoints = selected["points"]
        numbers = [allpoints[i]["x"] for i in range(len(allpoints))]
    if selected is None:
        numbers = [1]
    return numbers

def selection_to_mask(selected, image_size):
    width, height = image_size
    if selected is not None:
        allpoints = selected["points"]
        flat_indices = [allpoints[i]["pointNumbers"] for i in range(len(allpoints))]
        flat_indices = [item for sublist in flat_indices for item in sublist]
        y = [ind // height for ind in flat_indices]
        x = [ind % width for ind in flat_indices]
    if selected is None:
        x = [1]
        y = [1]
    return x, y

def overlay_labels(image, lbp, labels):
    mask = np.logical_or.reduce([lbp == each for each in labels])
    # image = to_grey_scale(image, dataset_name)
    return label2rgb(mask, image=image, bg_label=0, alpha=0.2)

def integer_to_binary(integer):
    binary_array = np.zeros(8)
    binary_string = np.binary_repr(integer)
    for idx in range(len(binary_string)):
        binary_array[-(idx+1)] = int(binary_string[-(idx+1)])
    return binary_array
