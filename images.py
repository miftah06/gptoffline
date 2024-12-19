import torch
from PIL import Image
import imageio
import requests
from io import BytesIO
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the Stable Diffusion model
MODEL_PATH = 'kl-f8-anime2.vae.pt'  # Update with the actual model path
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = torch.load(MODEL_PATH, map_location=device)

def generate_image_from_description(description):
    # Convert description to input tensor for the model
    # For demonstration purposes, we'll assume the model accepts text directly
    # Adjust the following as per the actual model input requirements
    input_tensor = torch.tensor([description]).to(device)

    with torch.no_grad():
        output = model(input_tensor)

    # Convert model output to image
    image_array = output.cpu().numpy()[0]
    image = Image.fromarray(np.uint8(image_array * 255))
    image = image.resize((512, 512))  # Resize for consistency
    return image

def generate_image_from_url(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch image from URL with status {response.status_code}: {response.text}")

    img = Image.open(BytesIO(response.content))
    img = img.resize((512, 512))  # Resize for consistency
    return img

def save_image(image, file_path):
    try:
        image.save(file_path)
        logging.debug(f'Image saved at: {file_path}')
    except IOError as e:
        logging.error(f"Error saving image: {e}")
        raise

def generate_image(description=None, url=None):
    if description:
        logging.debug(f"Generating image from description: {description}")
        image = generate_image_from_description(description)
    elif url:
        logging.debug(f"Generating image from URL: {url}")
        image = generate_image_from_url(url)
    else:
        raise ValueError("Either description or URL must be provided")

    file_path = 'generated_image.png'
    save_image(image, file_path)
    return file_path
