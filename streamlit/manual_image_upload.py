import streamlit as st
from PIL import Image
from torchvision import models, transforms
import torch

def show_manual_image_upload():
    
    #image uploader
    file_up = st.file_uploader("Upload an image", type="jpg")

    image = Image.open(file_up)
    st.image(image, caption='Uploaded Image', use_column_width=True)


    # EXAMPLE CHANGE TO OUR MODEL
    resnet = models.resnet101(pretrained=True)

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])

    # load the image, pre-process it, and make predictions
    img = Image.open(image_path)
    batch_t = torch.unsqueeze(transform(img), 0)
    resnet.eval()
    out = resnet(batch_t)

    # return the top 5 predictions ranked by highest probabilities
    prob = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)
    return [(classes[idx], prob[idx].item()) for idx in indices[0][:5]]










