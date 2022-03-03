from dataset import *
import torchvision.transforms as transforms


dataset = ETHDataset(transform=transforms.Compose([
                               # transforms.Resize(image_size),
                               transforms.CenterCrop([256,256]),
                               transforms.ToTensor(),
                           ]))





if __name__ == '__main__':
print("test")