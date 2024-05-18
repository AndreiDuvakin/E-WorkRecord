import random
from string import ascii_lowercase, digits

import cv2
import numpy as np
from flask import Flask, request, jsonify
from pytesseract import pytesseract
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = ''.join([random.choice(ascii_lowercase + digits) for _ in range(10)])


def preprocess_image_first(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (1, 1), 0)
    gray = cv2.convertScaleAbs(gray, alpha=1.6, beta=0)
    binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return binary_image


def preprocess_image_second(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gaussian_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    ret, thresh_img = cv2.threshold(gaussian_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh_img


def ocr_image(image):
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config, lang='rus')
    return text


@app.route('/recognition', methods=['POST'])
def text_recognition():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    response = []

    preprocessed_image = preprocess_image_first(img)
    text = ocr_image(preprocessed_image)
    response.append(text)

    preprocessed_image = preprocess_image_second(img)
    text = ocr_image(preprocessed_image)
    response.append(text)

    return jsonify(response)


def main():
    serve(app, host='0.0.0.0', port=6543)


if __name__ == '__main__':
    main()
