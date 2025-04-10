import torch
from torchvision import transforms
from inference.Inferencer import Inferencer
from models.PasticheModel import PasticheModel
from PIL import Image


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

num_styles = 16
image_size = 512
model_save_dir = "style16/pastichemodel-FINAL.pth"

pastichemodel = PasticheModel(num_styles)

inference = Inferencer(pastichemodel, device, image_size)
inference.load_model_weights(model_save_dir, device)

example_image_path = "temp/b.jpg"
im = Image.open(example_image_path).convert('RGB')

image = inference.eval_image(im, 5, 3, 1)

image.save("temp/b_out.jpg")