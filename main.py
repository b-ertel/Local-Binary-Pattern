from dataset import *
import torchvision.transforms as transforms


dataset = ETHDataset(transform=transforms.Compose([
                               # transforms.Resize(image_size),
                               transforms.CenterCrop([256,256]),
                               transforms.ToTensor(),
                           ]))

dataset.__getitem__(0)
dataset.get_path(0)
dataset.get_attribute_name(0)



if __name__ == '__main__':
    print("test")