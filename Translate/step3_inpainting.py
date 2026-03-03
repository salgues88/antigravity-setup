import cv2
import numpy as np
import os
from typing import List, Dict

def inpaint_image(image_path: str, bboxes: List[Dict], output_path: str = None) -> str:
    """
    1단계에서 정밀 탐지된 바운딩 박스를 마스크로 변환하여
    OpenCV의 Telea 알고리즘을 통해 텍스트를 자연스럽게 지우고 배경을 복원합니다.
    """
    if not os.path.exists(image_path):
        print(f"이미지를 찾을 수 없습니다: {image_path}")
        return image_path
        
    print(f"[{os.path.basename(image_path)}] 배경 복원(인페인팅) 가동 (총 {len(bboxes)}개 요소 지우기)")
        
    img = cv2.imread(image_path)
    if img is None:
        return image_path
        
    # 동일한 크기의 텅 빈 마스크(검은색 캔버스) 생성
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # 바운딩 박스 영역들을 하얀색(255)으로 칠해서 지울 영역 지정
    for bbox_info in bboxes:
        box_coords = bbox_info["box"]
        # polygon 좌표를 OpenCV가 인식하는 형태로 포맷팅
        pts = np.array(box_coords, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], 255)
        
    # 글씨 테두리 주변 픽셀까지 덮기 위해 구조적 팽창
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=3)
    
    # OpenCV Telea 알고리즘 식질
    inpainted_img = cv2.inpaint(img, dilated_mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
    
    if not output_path:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_cleaned{ext}"
        
    cv2.imwrite(output_path, inpainted_img)
    print(f"   [완료] 무손실 처리 이미지 생성: {os.path.basename(output_path)}")
    return output_path

if __name__ == "__main__":
    pass
