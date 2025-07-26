from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests
from bs4 import BeautifulSoup
import os, sys, io
import tempfile
import tensorflow_hub as hub
from flask_cors import CORS
import subprocess
import uuid

sys.stdout = io.StringIO()
sys.stderr = io.StringIO()

app = Flask(__name__)
CORS(app)

# Load model manually
print("Loading NSFW model...")
model = load_model("nsfw_mobilenet2.224x224.h5", custom_objects={'KerasLayer': hub.KerasLayer}, compile=False)
print("Model loaded successfully.")

LABELS = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']
BLOCKED_KEYWORDS = ["porn", "bet", "gamble", "xxx", "casino", "nsfw"]

def is_image_nsfw(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)

    preds = model.predict(img_array)[0]
    nsfw_score = preds[LABELS.index("porn")] + preds[LABELS.index("sexy")]
    print(f"[Frame NSFW Score] {img_path} → {nsfw_score:.2f}")

    return nsfw_score > 0.7

def is_url_nsfw(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        # --------- 1. Text-based keyword scan ---------
        page_text = soup.get_text().lower()
        flagged_keywords = [word for word in BLOCKED_KEYWORDS if word in page_text]
        print(f"[Keyword] Flagged keywords: {flagged_keywords}")

        # --------- 2. Image-based NSFW detection ---------
        images = soup.find_all("img")
        print(f"[INFO] Found {len(images)} images on {url}")

        for img_tag in images[:5]:  # Scan up to 5 images
            img_url = img_tag.get("src")
            if not img_url or not img_url.startswith("http"):
                continue

            try:
                img_data = requests.get(img_url, timeout=5).content
                with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
                    tmp.write(img_data)
                    tmp_path = tmp.name

                img = image.load_img(tmp_path, target_size=(224, 224))
                img_array = image.img_to_array(img)
                img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
                img_array = np.expand_dims(img_array, axis=0)

                preds = model.predict(img_array)[0]
                os.remove(tmp_path)

                nsfw_score = preds[LABELS.index("porn")] + preds[LABELS.index("sexy")]
                print(f"[Scan] {img_url} → NSFW score: {nsfw_score:.2f}")

                if nsfw_score > 0.7:
                    return True, flagged_keywords
            except Exception as img_error:
                print(f"[IMG ERROR] {img_url} → {img_error}")

        return False, flagged_keywords

    except Exception as e:
        print(f"[ERROR] Failed to scan {url}: {e}")
        return False, []

@app.route('/scan-url', methods=['POST'])
def scan_url():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    nsfw, flagged_keywords = is_url_nsfw(url)
    return jsonify({
        "nsfw": nsfw,
        "flagged_keywords": flagged_keywords
    })

@app.route('/scan-text', methods=['POST'])
def scan_text():
    try:
        data = request.get_json()
        text = data.get("text", "").lower()

        flagged_keywords = [word for word in BLOCKED_KEYWORDS if word in text]
        print(f"[Keyword] Flagged keywords from text: {flagged_keywords}")

        return jsonify({
            "nsfw": False,
            "flagged_keywords": flagged_keywords
        })
    except Exception as e:
        print(f"[ERROR] /scan-text failed: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/scan-frame', methods=['POST'])
def scan_frame():
    try:
        data = request.get_json()
        base64_image = data.get("image")

        if not base64_image:
            return jsonify({"error": "No image data provided"}), 400

        import base64
        from PIL import Image
        from io import BytesIO

        # Decode image
        image_data = base64.b64decode(base64_image.split(",")[1])
        img = Image.open(BytesIO(image_data))
        temp_path = f"frame_temp_{uuid.uuid4().hex}.jpg"
        img.save(temp_path)

        is_nsfw = is_image_nsfw(temp_path)
        os.remove(temp_path)

        return jsonify({"nsfw": is_nsfw})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#PRANK_SCRIPT = "prank.py"
PRANK_SCRIPT = "bsod.exe"

@app.route('/trigger-prank', methods=['POST'])
def trigger_prank():
    try:
        print("[TRIGGER] prank.py is launching...")
        #subprocess.Popen([sys.executable, "prank.py"])
        #os.system(f'python {PRANK_SCRIPT}')
        os.system(PRANK_SCRIPT)
        return jsonify({"status": "Prank launched"})
    except Exception as e:
        print(f"[ERROR] prank.py failed to launch: {e}")
        return jsonify({"error": str(e)}), 500
    
import threading

def start_file_monitoring():
    try:
        import nsfw_watchdog
        threading.Thread(target=nsfw_watchdog.start_monitoring, daemon=True).start()
        print("[Startup] File monitor launched.")
    except Exception as e:
        print(f"[Startup Error] Could not launch watchdog: {e}")

start_file_monitoring()

if __name__ == '__main__':
    app.run(port=6969)