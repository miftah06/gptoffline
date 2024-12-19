import requests
from PIL import Image
from io import BytesIO
import os

def fetch_search_results(query):
    # Example API call, replace with your actual API and processing logic
    response = requests.get(f'https://www.google.com/search?sca_esv=677ff2260c38da6a&sca_upv=1&sxsrf=ADLYWIJYOmDG1phZWIJFkd3pZDdTEV2J5g:1724203799061&q={query}&dpr=1.25')
    response.raise_for_status()
    return response.json()

def download_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

def save_image(img, filename):
    try:
        img.save(filename)
    except Exception as e:
        print(f"Error saving image: {e}")

def generate_images(query):
    results = fetch_search_results(query)
    
    for i, result in enumerate(results):
        image_url = result.get('image_url')
        if not image_url:
            continue
        
        img = download_image(image_url)
        if img:
            filename = f'image_{i}.png'
            save_image(img, filename)
            print(f"Image saved as {filename}")

def main():
    query = input("Enter search query: ")
    generate_images(query)

if __name__ == "__main__":
    main()
