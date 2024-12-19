import os
import requests
import logging
from datetime import datetime

IMAGE_FOLDER = 'static/images'
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def run_ai_model(url_description):
    # Simulated AI model call (replace with actual implementation)
    # Handle errors such as "Expecting value: line 1 column 1 (char 0)"
    try:
        # Simulate API call
        response = requests.get('http://localhost:1026/generate_image', params={'description': url_description})
        response.raise_for_status()
        
        # If the response content is empty, raise an error
        if not response.content:
            raise ValueError("Empty response from the AI model")
        
        # Simulate retrieving image URL from response
        image_url = response.json().get('image_url')
        if not image_url:
            raise ValueError("Invalid response format: 'image_url' key missing")

        return image_url

    except requests.RequestException as e:
        logging.error(f"Request error occurred: {e}")
        raise RuntimeError(f"Request error occurred: {e}")
    except ValueError as ve:
        logging.error(f"Value error occurred: {ve}")
        raise RuntimeError(f"Value error occurred: {ve}")
    except Exception as ex:
        logging.error(f"An unexpected error occurred: {ex}")
        raise RuntimeError(f"An unexpected error occurred: {ex}")

def generate_and_save_image(url_description):
    try:
        image_url = run_ai_model(url_description)
        
        # Save the generated image
        output_path = os.path.join(IMAGE_FOLDER, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_generated_image.png")
        with open(output_path, 'wb') as f:
            response = requests.get(image_url)
            response.raise_for_status()  # Ensure the request was successful
            f.write(response.content)

        # Example: delete the response object to free memory if needed
        del response

        return f'/static/images/{os.path.basename(output_path)}'
    except Exception as e:
        logging.error(f"Error in generate_and_save_image: {e}")
        return None
