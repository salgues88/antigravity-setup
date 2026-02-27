import cv2
import numpy as np
import os

def remove_text_and_inpaint(image_path: str, text_boxes: list) -> np.ndarray:
    """
    이미지 경로와 OCR로 추출된 바운딩 박스(좌표) 목록을 인자로 받아,
    해당 텍스트 영역을 하얗게 지우고 주변 픽셀을 이용해 조잡하지 않게 배경(식질)을 복원합니다.
    
    Args:
        image_path: 원본 이미지 파일의 경로
        text_boxes: [{'box': [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]}, ...] 형식의 리스트
        
    Returns:
        np.ndarray: 배경이 복원(Inpainting)된 OpenCV 이미지 객체 배열
    """
    try:
        # 이미지 읽기 (한글 경로 깨짐 방지를 위해 numpy를 통한 우회 로드 - OpenCV의 한계 극복)
        stream = open(image_path, "rb")
        bytes_array = bytearray(stream.read())
        numpy_array = np.asarray(bytes_array, dtype=np.uint8)
        img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
        stream.close()

        if img is None:
            raise FileNotFoundError(f"이미지를 불러올 수 없습니다: {image_path}")

        # 원본 이미지와 동일한 크기의 검은색 캔버스(단일 채널) 생성 -> 마스크용
        mask = np.zeros(img.shape[:2], dtype=np.uint8)

        # 각 OCR 박스 영역을 마스크에 하얗게(255) 칠함
        for item in text_boxes:
            box = item['box']
            # Float 좌표를 Int 좌표 평면으로 변환
            pts = np.array(box, dtype=np.int32)
            # 글씨 주변 여백까지 덮기 위해 다각형 내부를 색칠 (좀 더 깨끗하게 지우기 위함)
            # 테두리를 조금 더 넉넉히 잡기 위한 약간의 팽창(Dilation) 고려
            cv2.fillPoly(mask, [pts], (255))
            
        # 마스크(텍스트 영역) 팽창 작용: 글자 주변의 테두리, 안티앨리어싱 잔재까지 포함하도록 범위 확장
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        mask_dilated = cv2.dilate(mask, kernel, iterations=1)

        print(f"[{image_path}] 텍스트 영역 마스킹 완료, 배경 Inpainting 복원 시작...")
        
        # Telea 알고리즘 (또는 INPAINT_NS)을 사용하여 배경 복원
        # inpaintRadius: 주변 몇 픽셀을 참조할 것인가 (만화 톤의 크기에 따라 조정 필요, 기본 3~5가 적당)
        inpainted_img = cv2.inpaint(img, mask_dilated, inpaintRadius=5, flags=cv2.INPAINT_TELEA)
        
        print(f"[{image_path}] 배경 복원 완료.")
        return inpainted_img

    except Exception as e:
        print(f"[Inpainting 에러] 배경 복원 중 오류 발생 ({image_path}): {e}")
        # 실패 시 원본 그대로 리턴하거나 빈 배열 리턴
        return None

if __name__ == "__main__":
    # 단독 테스트 코드
    test_img = "test.jpg"
    test_boxes = [
        {'box': [[50, 50], [150, 50], [150, 100], [50, 100]], 'text': 'サンプル'}
    ]
    if os.path.exists(test_img):
        res_img = remove_text_and_inpaint(test_img, test_boxes)
        if res_img is not None:
            cv2.imshow("Inpainted Result", res_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("테스트할 이미지가 없습니다.")
