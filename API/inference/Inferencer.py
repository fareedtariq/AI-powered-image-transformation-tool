import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms, utils
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from glob import glob
import warnings

warnings.filterwarnings("ignore")

# import matplotlib.pyplot as plt
# from matplotlib.pyplot import imshow
import time
import os
import copy
import pandas as pd
from PIL import Image
from skimage import io, transform
import random
from tqdm import tqdm
from sklearn.utils import shuffle
from random import randint

# from dataloaders.PhotoDataset import PhotoDataset
from models.Vgg16FeatureModel import Vgg16FeatureModel
from models.PasticheModel import ResBlock, CondConvolution, Upsampling, PasticheModel
from collections import defaultdict


class Inferencer(object):
    def __init__(self, pastiche_model, device, image_size):
        self.pastichemodel = pastiche_model
        self.device = device

        self.pastichemodel = self.pastichemodel.to(self.device)
        self.pastichemodel = self.pastichemodel.eval()

        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]

        self.transformer = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean,
                                 std=self.std)
        ])

    def load_model_weights(self, dir_model, device='cuda'):
        self.pastichemodel.load_state_dict(torch.load(dir_model, map_location=device))

    def eval_image(self, img, style_num, style_num2=None, alpha=None):
        out = self.transformer(img)
        # res = self.pastichemodel(out.unsqueeze(0).to(self.device), style_num, style_num2, alpha)
        res = self.pastichemodel(out.unsqueeze(0).to(self.device), style_num, style_num2, alpha)
        res_img = Image.fromarray(np.uint8(np.moveaxis(res[0].cpu().detach().numpy() * 255.0, 0, 2)))

        return res_img