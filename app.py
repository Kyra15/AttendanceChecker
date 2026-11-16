from flask import Flask, render_template, request, jsonify
# import OCR_utility
import cohere
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64
import binascii
import cv2
from PIL import Image
import numpy as np
import io
import pillow_heif
from concurrent.futures import ThreadPoolExecutor


load_dotenv()
pillow_heif.register_heif_opener()

api_key = os.environ.get("API_KEY")
co = cohere.ClientV2(api_key) if api_key else None

PROMPT_OCR = (
    "Transcribe every piece of visible text in this image exactly as it "
    "appears, in reading order. Do not summarize, explain, or add commentary."
    "Output only the transcribed text."
)

app = Flask(__name__)
CORS(app)


class ImgError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code
        self.message = message



def decode_image(image_base64):
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]

    image_bytes = base64.b64decode(image_base64)
    np_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        # opencv can't read heic, fall back to pillow (ios photos)
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    return image


def read_page(image_base64):
    try:
        image = decode_image(image_base64)
    except (binascii.Error, ValueError, OSError, cv2.error, Image.DecompressionBombError):
        raise ImgError("unreadable", "That image could not be opened. Try retaking it.")
    
    success, encoded_img = cv2.imencode(".jpg", image)
    if not success:
        raise ImgError("unreadable", "That image could not be processed. Try retaking it.")

    data_uri = "data:image/jpeg;base64," + base64.b64encode(encoded_img).decode("utf-8")

    try:
        response = co.chat(
            model="command-a-vision-07-2025",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT_OCR},
                        {
                            "type": "image_url",
                            "image_url": {"url": data_uri, "detail": "high"},
                        },
                    ],
                }
            ],
            temperature=0.0,
        )
    except Exception as e:
        raise ImgError("ocr_failed", "The reader is having trouble right now. Try again in a second")

    parts = response.message.content or []
    text = parts[0].text.strip() if parts else ""
    if not text:
        raise ImgError("no_text", "No text was found. Make sure the lab report fills the frame.")
    return text


@app.route('/')
def index():
    return render_template('index.html', title='Attendance Checker')


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "cohere": co is not None})


@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json(silent=True) or {}
    images = data.get("images")

    if images is None and data.get("imageBase64"):
        images = [data["imageBase64"]]

    def run(numbered):
        page, b64 = numbered
        try:
            return page, read_page(b64), None
        except ImgError as e:
            return page, None, e

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(run, enumerate(images, start=1)))

    texts = [text for _, text, err in results if err is None]

    return jsonify(texts)


if __name__ == '__main__':
    app.run(debug=True)
