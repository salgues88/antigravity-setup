import torch  # WinError 127 (shm.dll 충돌) 방지를 위해 paddleocr보다 먼저 import
from paddleocr import PaddleOCR
import numpy as np
import cv2
import os

# 디버그 모드 비활성화 및 일본어 특화 OCR 인스턴스 초기화
# use_angle_cls=True 로 설정하여 세로쓰기 등 방향성 탐지 정확도 극대화
try:
    ocr_engine = PaddleOCR(use_angle_cls=True, lang='japan', show_log=False)
except Exception as e:
    print(f"PaddleOCR 초기화 오류: {e}")
    ocr_engine = None

def detect_text_boxes(image_path: str) -> list:
    """
    주어진 이미지에서 텍스트의 바운딩 박스(좌표)만을 정밀하게 짚어냅니다.
    반환 포맷: [{"box": [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]}, ...]
    """
    if ocr_engine is None:
        return []

    if not os.path.exists(image_path):
        print(f"이미지를 찾을 수 없습니다: {image_path}")
        return []
        
    print(f"[{os.path.basename(image_path)}] PaddleOCR 텍스트 스파팅 중...")
    
    # 텍스트 추출 (결과는 리스트 리스트 튜플 형태)
    result = ocr_engine.ocr(image_path, cls=True)
    
    bboxes = []
    
    if result and result[0]:
        for line in result[0]:
            # line[0]은 4개의 점으로 된 폴리곤 좌표 [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            box_coords = line[0]
            
            # 각 좌표값을 정수형으로 변환 보장
            int_box = []
            for point in box_coords:
                int_box.append([int(point[0]), int(point[1])])
                
            bboxes.append({"box": int_box})
            
    return bboxes

if __name__ == "__main__":
    # 단독 실행 시 테스트 로직
    test_img = "test_images/Gallery_Fake_33_003.jpg"
    boxes = detect_text_boxes(test_img)
    
    if boxes:
        img = cv2.imread(test_img)
        for b in boxes:
            pts = np.array(b["box"], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0, 0, 255), 3)
            
        cv2.imwrite("debug_paddle_boxes.jpg", img)
        print(f"총 {len(boxes)}개의 박스를 마스킹하여 'debug_paddle_boxes.jpg'로 저장했습니다.")
    else:
        print("텍스트 박스를 찾지 못했습니다.")
