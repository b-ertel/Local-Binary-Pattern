from PIL import Image
import numpy as np
from skimage.color import label2rgb

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
        numbers = [1,2]
    return numbers

def selection_to_mask(selected):
    if selected is not None:
        image_size = 256
        allpoints = selected["points"]
        flat_indices = [allpoints[i]["pointNumbers"] for i in range(len(allpoints))]
        flat_indices = [item for sublist in flat_indices for item in sublist]
        y = [ind // 256 for ind in flat_indices]
        x = [ind % 256 for ind in flat_indices]
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
