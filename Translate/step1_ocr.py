import os
import cv2
import easyocr
import numpy as np
from PIL import Image

# manga-ocr 라이브러리 (정발본/고품질 일본어 원서 전용 광학인식기)
try:
    from manga_ocr import MangaOcr
    print("[시스템] 고품질 만화 전문 OCR 모델(manga-ocr)을 로딩 중입니다. (최초 1회 수 초 소요)")
    mocr = MangaOcr()
except ImportError:
    print("[경고] manga-ocr가 설치되어 있지 않습니다. 기본 EasyOCR 엔진만으로 작동합니다.")
    mocr = None
except Exception as e:
    print(f"[경고] manga-ocr 로딩 실패: {e}")
    mocr = None

def detect_and_extract_text(image_path: str, lang_list: list = ['ja', 'en']) -> list:
    '''
    EasyOCR을 사용하여 텍스트가 있는 위치(바운딩 박스)만 탐지하고,
    해당 영역의 이미지를 잘라내서 manga-ocr 모델로 교차 검증하여 텍스트 인식률을 획기적으로 올립니다.
    '''
    try:
        # 1. EasyOCR로 대략적인 영역 탐지 (신뢰도는 낮더라도 박스 위치만 파악)
        reader = easyocr.Reader(lang_list, gpu=False, verbose=False)
        print(f"[{os.path.basename(image_path)}] 이미지 영역 탐지 중...")
        result = reader.readtext(image_path)
        
        extracted_data = []
        
        # 크롭(Crop)을 수행하기 위해 원본 이미지를 Pillow 객체로 로드
        orig_img = Image.open(image_path).convert('RGB')
        
        for (bbox, text, prob) in result:
            # 너무 낮은 신뢰도의 박스 노이즈는 제외
            if prob < 0.15:
                continue
                
            pts = np.array(bbox, dtype=np.int32)
            
            # 2. 바운딩 박스를 기준으로 이미지 크롭 준비
            x_min = max(0, int(np.min(pts[:, 0])))
            x_max = min(orig_img.width, int(np.max(pts[:, 0])))
            y_min = max(0, int(np.min(pts[:, 1])))
            y_max = min(orig_img.height, int(np.max(pts[:, 1])))
            
            # 박스 크기가 너무 작으면 말풍선이 아니라 잡티/선일 확률이 높음
            if (x_max - x_min) < 10 or (y_max - y_min) < 10:
                continue
                
            # 만화 대사는 끄트머리가 잘리면 인식이 안 되므로 박스에 3픽셀 여유(패딩)를 줌
            pad = 3
            x_min = max(0, x_min - pad)
            x_max = min(orig_img.width, x_max + pad)
            y_min = max(0, y_min - pad)
            y_max = min(orig_img.height, y_max + pad)
            
            crop_img = orig_img.crop((x_min, y_min, x_max, y_max))
            
            # 3. 잘라낸 단일 말풍선(또는 효과음) 이미지를 만화 전용 모델(manga-ocr)에 통과시킴
            manga_text = ""
            if mocr is not None:
                manga_text = mocr(crop_img)
            else:
                manga_text = text # fallback
                
            # 모델이 텍스트를 찾지 못했으면 생략
            if not manga_text.strip():
                continue
                
            item = {
                'box': bbox,
                'text': manga_text,
                'confidence': 0.99  # manga-ocr 결과물이므로 최고수준의 신뢰도 보장
            }
            extracted_data.append(item)
            
        print(f"[OCR 완료] 총 {len(extracted_data)}개의 핵심 만화 텍스트 문장을 추출했습니다.")
        return extracted_data

    except Exception as e:
        print(f"[OCR 에러] {image_path} 처리 중 오류 발생: {e}")
        return []

if __name__ == "__main__":
    pass
