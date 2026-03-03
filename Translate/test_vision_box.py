import os
import google.generativeai as genai
from PIL import Image, ImageDraw
import json

api_key = "AIzaSyACj_8hNqYaZkTbQKAZ0RDgyP1DriLYkUA"
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

img_path = "test_images/Gallery_Fake_33_003.jpg"
image = Image.open(img_path)

prompt = """
You are a professional manga translator and an expert computer vision model. Analyze this Japanese manga page image.
CRITICAL MISSION: You must find ALL text in the image accurately without overlaps. Manga contains two types of text:
1. Vertical Text (Tategaki - 縦書き): Read from top to bottom, right to left.
2. Horizontal Text (Yokogaki - 横書き): Read from left to right.

For EVERY text block, you MUST return its precise bounding box coordinates in [ymin, xmin, ymax, xmax] format scaled to 0-1000.

CRITICAL RULES for Bounding Boxes:
- RULE 1 (NO OVERLAP): Bounding boxes MUST NEVER OVERLAP with each other. Different text blocks are always physically separate.
- RULE 2 (TIGHT FIT): The bounding box must tightly enclose ONLY the text characters, not the surrounding whitespace or empty parts of the speech bubble.
- RULE 3 (VERTICAL TEXT): For VERTICAL text (height > width), enclose the entire vertical column(s) of the sentence perfectly. Do not slice a single vertical sentence into multiple boxes. 
- RULE 4 (HORIZONTAL TEXT): For HORIZONTAL text (width > height), be extremely precise. Do not mistakenly group distinct horizontal lines, and strictly exclude adjacent artworks or blank spaces.

Also provide the original Japanese text and its natural Korean translation (as a professional translator for the manga 'Gallery Fake').

Return ONLY a valid JSON array. Do not include any markdown formatting like ```json or ```.
[
  {
    "box_2d": [ymin, xmin, ymax, xmax],
    "japanese": "...",
    "korean": "..."
  }
]
"""

try:
    print("Gemini API 호출 중...")
    response = model.generate_content([prompt, image])
    text = response.text
    
    # JSON 파싱 준비
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].strip()
        
    data = json.loads(text)
    
    # 디버그용 이미지에 박스 그리기
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    extracted_results = []
    
    for item in data:
        y1, x1, y2, x2 = item["box_2d"]
        
        # 0~1000 상대 좌표를 실제 이미지 픽셀 해상도 좌표로 변환
        px1 = int((x1 / 1000) * width)
        py1 = int((y1 / 1000) * height)
        px2 = int((x2 / 1000) * width)
        py2 = int((y2 / 1000) * height)
        
        draw.rectangle([px1, py1, px2, py2], outline="red", width=3)
        extracted_results.append({
            "box": [[px1, py1], [px2, py1], [px2, py2], [px1, py2]],
            "korean": item.get("korean", "")
        })
        
    image.save("debug_boxes.jpg")
    print(f"✅ 디버그 이미지 저장 완료: debug_boxes.jpg (총 {len(data)}개의 텍스트 감지됨)")
    print(json.dumps(extracted_results, ensure_ascii=False, indent=2))
        
except Exception as e:
    print(f"오류 발생: {e}")
