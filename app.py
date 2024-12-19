from flask import Flask, request, jsonify, send_from_directory, render_template
import requests
import logging
import os
from PIL import Image, ImageEnhance
from io import BytesIO
from datetime import datetime
import subprocess
from image_generator import generate_image_from_text, generate_image_from_url  

app = Flask(__name__)

# Configuration for AI model
AI_MODEL_URL = 'https://api.cloudflare.com/client/v4/accounts/eb9851ec9c1f1597dffa745472e33984/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0'
WORKERS_API_TOKEN =  'harap di isi'

# Configuration for Google Custom Search
GOOGLE_API_KEY = 'cari di google cloud'
GOOGLE_CX = '46198aef1648f472d'
IMAGE_FOLDER = 'static/images'

os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Setup logging configuration
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route('/images')
def images():
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith('.jpg')]
    return jsonify(image_files)

@app.route('/dorking', methods=['POST'])
def dorking():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    endpoint = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CX,
        'searchType': 'image',
        'q': query,
        'num': 10
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        image_urls = [item['link'] for item in data.get('items', [])]
        return jsonify({'image_urls': image_urls or []})
    except requests.HTTPError as e:
        logging.error(f"Request error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('query')
    if not prompt:
        return jsonify({"error": "Query is required."}), 400

    try:
        image = generate_image_from_text(prompt)
        if image:
            image_path = os.path.join(IMAGE_FOLDER, f"{datetime.now():%Y%m%d_%H%M%S}_image.jpg")
            image.save(image_path)
            return jsonify({'image_path': image_path})
        else:
            return jsonify({"error": "Failed to generate image."}), 500
    except Exception as e:
        logging.error(f"Image generation failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/sharpen_image', methods=['POST'])
def sharpen_image():
    image_url = request.form.get('image_url')
    if not image_url:
        return jsonify({'error': 'No image URL provided'}), 400

    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(2.0)  # Increase sharpness
        img_path = os.path.join(IMAGE_FOLDER, f'sharpened_{datetime.now():%Y%m%d_%H%M%S}.jpg')
        img.save(img_path)
        
        return jsonify({'sharpened_image_url': f'/static/images/{os.path.basename(img_path)}'})
    except Exception as e:
        logging.error(f"Error sharpening image: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'Missing query'}), 400

    try:
        ai_response = run_ai_model(query)
        return jsonify({'ai_response': ai_response})
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return jsonify({'error': str(e)}), 500

def run_ai_model(prompt):
    headers = {'Authorization': f'Bearer {WORKERS_API_TOKEN}', 'Content-Type': 'application/json'}
    payload = {'prompt': prompt}

    try:
        response = requests.post(AI_MODEL_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('result') or 'No response from AI model.'
    except Exception as e:
        logging.error(f'Error calling AI model: {e}')
        return 'Error interacting with AI model.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1026, debug=True)
