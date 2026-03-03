import os
import google.generativeai as genai
from PIL import Image
import json

api_key = "AIzaSyACj_8hNqYaZkTbQKAZ0RDgyP1DriLYkUA"
genai.configure(api_key=api_key)

# Gemini 2.5 Flash 모델을 사용하여 다이렉트로 OCR 및 번역 시도
model = genai.GenerativeModel('gemini-2.5-flash')

img_path = "test_images/Gallery_Fake_33_003.jpg"
image = Image.open(img_path)

prompt = """
You are a professional manga translator. Analyze this manga page image.
Act as an OCR and translator. Find all the speech bubbles and sound effects.
For each text you find, return its bounding box coordinates in [ymin, xmin, ymax, xmax] format scaled to 0-1000.
Also provide the original Japanese text and its natural Korean translation.

Output strictly as a JSON array of objects. Example format:
[
  {
    "box_2d": [ymin, xmin, ymax, xmax],
    "japanese": "original text",
    "korean": "translated text"
  }
]
"""

print(f"[{img_path}] Gemini 1.5 Pro Vision API 테스트 시작...")

try:
    response = model.generate_content([prompt, image])
    print("--- Gemini API 응답 ---")
    print(response.text)
except Exception as e:
    print(f"에러 발생: {e}")
