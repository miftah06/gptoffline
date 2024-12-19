import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import requests
from io import BytesIO

# Konfigurasi model
MODEL_PATH = 'kl-f8-anime2.vae.pt'  # Replace this with the correct path to your model
DEVICE = 'cpu'  # Use CPU by default for ARM, as Snapdragon GPU support isn't directly available in PyTorch (requires native SDKs like SNPE)

# If running on a mobile device, ensure PyTorch Mobile is installed:
torch.device("cpu") #as no CUDA support on Android

# Load the Stable Diffusion model using PyTorch Mobile
# Stable Diffusion requires a lot of resources; thus, it is unlikely to run efficiently on mobile devices.
# You can attempt to use a smaller model or optimized version for mobile devices

def load_model():
    # Ensure to use a reduced model or one optimized for mobile
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", use_auth_token=True)
    model.to(DEVICE)
    return model

def generate_image_from_text(text):
    # Initialize the model
    model = load_model()

    # Generate the image using the provided text input
    with torch.no_grad():
        image = model(text).images[0]
        return image

def generate_image_from_url(url):
    # Fetch and process the image from the provided URL
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

if __name__ == "__main__":
    # Example usage
    prompt = "A scenic mountain view"
    generated_image = generate_image_from_text(prompt)
    generated_image.show()  # Display the generated image
