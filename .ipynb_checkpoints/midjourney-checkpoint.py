import requests
import os
import base64
from PIL import Image
from io import BytesIO

# Stable Diffusion API設定
STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

def send(prompt, width=512, height=512, steps=30, cfg_scale=7.5):
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json"
    }

    # multipart/form-data で送るべきフィールド
    files = {
        'prompt': (None, prompt),
        'output_format': (None, 'png'),
        'steps': (None, str(steps)),
        'cfg_scale': (None, str(cfg_scale)),
        'width': (None, str(width)),
        'height': (None, str(height))
    }

    response = requests.post(STABILITY_API_URL, headers=headers, files=files)

    if response.status_code == 200:
        print("Request successful!")
        image_base64 = response.json()['image']
        return image_base64
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        return None

def download_image(base64_data, save_path):
    try:
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        image.save(save_path)
        print(f"Image saved to {save_path}")
        return image
    except Exception as e:
        print(f"Error saving image: {e}")
       