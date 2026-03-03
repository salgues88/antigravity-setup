import google.generativeai as genai
from PIL import Image
import time
import random
import os
from typing import List, Dict

# 사용자가 제공한 무료 키 연결 (Generative AI 전용)
API_KEY = "AIzaSyACj_8hNqYaZkTbQKAZ0RDgyP1DriLYkUA"
genai.configure(api_key=API_KEY)

# 빠른 처리 및 비전 특화인 Flash 모델 배정
model = genai.GenerativeModel('gemini-2.5-flash')

def sleep_with_jitter(min_sec=3.5, max_sec=8.2):
    """
    [안티-디텍션 분산 알고리즘]
    API 서버에서 매크로나 봇으로 탐지(Ban)하는 것을 회피하기 위해
    호출 간의 지연 시간을 랜덤(난수)하게 부여하는 사람 모방 Jittering 함수입니다.
    """
    sleep_time = random.uniform(min_sec, max_sec)
    print(f"   [Anti-Detection] 봇 탐지 회피를 위해 {sleep_time:.2f}초간 휴식합니다...")
    time.sleep(sleep_time)

def crop_image(img_path: str, box: list, padding=15):
    """주어진 폴리곤 좌표 박스를 기준으로 이미지를 오려냅니다."""
    img = Image.open(img_path)
    
    # 박스 [ [x1, y1], [x2, y1], [x2, y2], [x1, y2] ] 좌표에서 Min/Max 구하기
    x_coords = [p[0] for p in box]
    y_coords = [p[1] for p in box]
    
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)
    
    # 약간의 여백(Padding)을 주어 제미니가 글씨 모양을 더 잘 인식하도록 함
    left = max(0, xmin - padding)
    top = max(0, ymin - padding)
    right = min(img.width, xmax + padding)
    bottom = min(img.height, ymax + padding)
    
    return img.crop((left, top, right, bottom))

def translate_boxes(image_path: str, bboxes: List[Dict]) -> List[Dict]:
    """
    1단계에서 정밀 탐지된 바운딩 박스를 순회하며:
    1. 이미지를 박스 단위로 크롭(오려냄)
    2. 생성된 이미지 파편을 제미니 VLM에 인코딩 전송
    3. 네이티브 인식 + 번역 결과 반환
    """
    if not bboxes:
        return []

    print(f"\n[{os.path.basename(image_path)}] VLM 하이브리드 번역기 가동 (총 {len(bboxes)}개 객체)")
    
    translated_data = []
    
    # 프롬프트: OCR과 번역을 동시에 수행하도록 강력한 룰 부여
    prompt = """
    You are a professional manga translator for the manga 'Gallery Fake'.
    Read the Japanese text present in this specific cropped image.
    1. Extract ONLY the Japanese text accurately.
    2. Translate it into natural, high-quality Korean.
    Return ONLY a valid JSON format like this, with NO markdown or other text:
    {"japanese": "...", "korean": "..."}
    """
    
    for i, bbox_info in enumerate(bboxes):
        box_coords = bbox_info["box"]
        cropped_img = crop_image(image_path, box_coords)
        
        print(f" -> {i+1}/{len(bboxes)} 번째 말풍선 조각 번역 중...")
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # 제미니 VLM에게 조각 이미지와 프롬프트를 동시 전송 (네이티브 인식)
                response = model.generate_content([prompt, cropped_img])
                res_text = response.text.strip()
                
                # 마크다운 ```json 찌꺼기 제거
                if res_text.startswith("```json"):
                    res_text = res_text[7:]
                if res_text.endswith("```"):
                    res_text = res_text[:-3]
                    
                import json
                try:
                    parsed = json.loads(res_text.strip())
                    bbox_info["japanese"] = parsed.get("japanese", "")
                    bbox_info["korean"] = parsed.get("korean", "")
                    translated_data.append(bbox_info)
                    print(f"      [성공] 번역본: {bbox_info['korean']}")
                    break # 성공 시 재시도 루프 탈출
                except json.JSONDecodeError:
                     print(f"      [오류] JSON 파싱 실패. (결과: {res_text})")
                     if attempt == max_retries - 1:
                         bbox_info["korean"] = ""
                         translated_data.append(bbox_info)
                         
            except Exception as e:
                print(f"      [API 에러] {e}")
                if attempt == max_retries - 1:
                    bbox_info["korean"] = ""
                    translated_data.append(bbox_info)
                else:
                    sleep_with_jitter(10.0, 15.0) # 에러 시 롱 브레이크
                    
        # 난수 수면으로 사용자 API 계정 보호 (Anti-detection)
        if i < len(bboxes) - 1:
            sleep_with_jitter(1.2, 3.8)
            
    return translated_data
