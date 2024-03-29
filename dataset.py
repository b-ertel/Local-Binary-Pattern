# from torch.utils.data import Dataset
from PIL import Image
import os
import pandas

class ETHDataset():
    """Dataset class for the flash images from the ETH synthesizability repository"""
    def __init__(self, img_dir = os.path.join("data", "ETH_Synthesizability", "texture"), transform=None, number_of_items = 7424):
        metadata = pandas.read_csv(f"data/eth_labels.csv")
        self.metadata = metadata[metadata.quality > 0.5].reset_index()
        # if number_of_items is not None:
        #     self.metadata  = self.metadata.sample(number_of_items)
        self.img_dir = img_dir
        self.transform = transform
        self.labelmap = {"animal": 0,
            "apple": 1,
            "bees": 2,
            "birds": 3,
            "biscuit": 4,
            "brick": 5,
            "cake": 6,
            "canvas": 7,
            "cardboard": 8,
            "carpet": 9,
            "chips": 10,
            "circular": 11,
            "cliff": 12,
            "cloud": 13,
            "concrete": 14,
            "cracked": 15,
            "crowd": 16,
            "crushed": 17,
            "crushed+stone": 18,
            "fabric": 19,
            "flakes": 20,
            "floor": 21,
            "flour": 22,
            "flow": 23,
            "flower": 24,
            "foam": 25,
            "food": 26,
            "fur": 27,
            "glass": 28,
            "grass": 29,
            "hair": 30,
            "leather": 31,
            "leaves": 32,
            "lined": 33,
            "marble": 34,
            "metal": 35,
            "mosaic": 36,
            "painting": 37,
            "paper": 38,
            "pasta": 39,
            "plastic": 40,
            "quartz": 41,
            "rain": 42,
            "rust": 43,
            "sand": 44,
            "satellite": 45,
            "stone": 46,
            "storm+light": 47,
            "texture": 48,
            "tile": 49,
            "urban": 50,
            "wall": 51,
            "water": 52,
            "wood": 53,
            "wool": 54,
            "woven": 55
        }

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        material = self.metadata.iloc[idx]["name"]
        material_name = material.split("_")[1].lower()
        material_attributes = self.labelmap[material_name]
        image_path = os.path.join(self.img_dir, f"{material}.jpg")
        # print(image_path)
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        # image = image.permute(1,2,0).numpy()
        return image, material_attributes  #, image_path

    def get_path(self, idx):
        material = self.metadata.iloc[idx]["name"]
        image_path = os.path.join(self.img_dir, f"{material}.jpg")
        return image_path

    def get_attribute_name(self, idx):
        material = self.metadata.iloc[idx]["name"]
        material_attributes = material.split("_")[1]
        return material_attributes.lower()





class BrodatzDataset():
    """Dataset class for the flash images from the Brodatz repository"""
    def __init__(self, img_dir = "data/textures", size = 400):
        self.metadata = pandas.read_csv(f"data/brodatz_labels.csv", header = None)
        # if number_of_items is not None:
        #     self.metadata  = self.metadata.sample(number_of_items)
        self.img_dir = img_dir
        self.size = size

    def __len__(self):
        return len(self.metadata)

    def __getitem__(self, idx):
        material = self.metadata.iloc[idx][2]
        img_name = self.metadata.iloc[idx][0]
        image_path = os.path.join(self.img_dir, f"{img_name}")
        # print(image_path)
        image = Image.open(image_path)
        width, height = image.size
        small_side = image.size[0] if image.size[0] < image.size[1] else image.size[1]
        left = (image.size[0]-small_side)//2
        top = (image.size[1]-small_side)//2
        image = image.crop((left,top,left + self.size, top + self.size))
        return image, material  #, image_path

    def get_path(self, idx):
        img_name = self.metadata.iloc[idx][0]
        image_path = os.path.join(self.img_dir, f"{img_name}")
        return image_path

    def get_attribute_name(self, idx):
        material = self.metadata.iloc[idx][2]
        return material.lower()