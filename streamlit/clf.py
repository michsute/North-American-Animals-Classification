from torchvision import transforms
from PIL import Image
import torch
from torchvision import models


def predict(image_path, model_path, classes_file):
    
    # Define the model architecture
    model = models.resnet50(pretrained=False)  # Replace with your specific model
    model.fc = torch.nn.Linear(model.fc.in_features, 12)  # Update for your number of classes

    # Load the saved state_dict
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Set to evaluation mode


    # Transformations for the input image (match training preprocessing)
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # Match the mean/std used during training
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Load and preprocess the image
    img = Image.open(image_path).convert("RGB")  # Ensure the image has 3 channels
    batch_t = torch.unsqueeze(transform(img), 0)

    # Perform inference
    with torch.no_grad():  # Disable gradient computation
        out = model(batch_t)

    # Load class labels
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    # Calculate probabilities and get top predictions
    prob = torch.nn.functional.softmax(out, dim=1)[0] * 100
    _, indices = torch.sort(out, descending=True)

    return [(classes[idx], prob[idx].item()) for idx in indices[0][:5]]
