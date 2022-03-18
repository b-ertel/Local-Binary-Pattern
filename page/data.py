from dataset import *


# ############CONFIGS, DATA, ETC #####################################
# dataset = BrodatzDataset(transform=transforms.Compose([
#                                # transforms.Resize(image_size),
#                                transforms.CenterCrop([256,256]),
#                            ]))
#

dataset = BrodatzDataset()
dataset_name = "brodatz"

# dataset = ETHDataset(transform=transforms.Compose([
#                                # transforms.Resize(image_size),
#                                transforms.CenterCrop([256,256]),
#                                # transforms.ToTensor(),
#                            ]))
#
# dataset_name = "eth"
