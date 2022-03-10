from dataset import *
import torchvision.transforms as transforms


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
