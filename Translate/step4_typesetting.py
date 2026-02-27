import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import re

def draw_korean_text_on_image(inpainted_cv2_img: np.ndarray, text_boxes: list, translated_texts: list, font_path: str = None) -> np.ndarray:
    """
    배경이 지워진 이미지 위에, 지정된 좌표를(말풍선) 기준으로 번역된 한국어 텍스트를 
    자동 줄바꿈(Word wrap) 및 중앙 정렬 처리하여 자연스럽게 그려 넣습니다.
    
    Args:
        inpainted_cv2_img: `3_inpainting.py`에서 반환된 글씨 지워진 OpenCV 배열 이미지 (BGR)
        text_boxes: OCR 추출 원본 바운딩 박스 목록
        translated_texts: 번역된 한국어 텍스트 목록의 리스트
        font_path: 사용할 .ttf 폰트 파일의 절대경로 (지정 안 하면 시스템 기본 고딕 사용)
        
    Returns:
        np.ndarray: 완성된(식질+조판) 최종 OpenCV 배열 이미지
    """
    if inpainted_cv2_img is None:
        raise ValueError("입력된 빈 이미지가(cv2) 존재하지 않습니다.")
    
    # BGR(OpenCV) -> RGB(Pillow) 변환
    img_rgb = cv2.cvtColor(inpainted_cv2_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(pil_img)

    for i, (box_item, text) in enumerate(zip(text_boxes, translated_texts)):
        # 좌표 추출
        box = np.array(box_item['box'])
        x_coords = box[:, 0]
        y_coords = box[:, 1]
        
        # 말풍선의 대략적인 경계 (X 최솟값, X 최댓값, Y 최솟값, Y 최댓값)
        min_x, max_x = int(np.min(x_coords)), int(np.max(x_coords))
        min_y, max_y = int(np.min(y_coords)), int(np.max(y_coords))
        
        # 말풍선의 너비와 높이
        box_width = max_x - min_x
        box_height = max_y - min_y
        
        # 폰트 크기 동적 조절 (말풍선 크기와 글자 길이에 반비례하게 대략적 계산)
        # 16은 최소, 박스 높이의 1/3을 최대로 두는 경험적 수치
        font_size = max(16, min(int(box_height / 3), int(box_height * box_width / (len(text) * 40 + 1))))
        
        try:
            # 윈도우 시스템에서 쓸만한 기본 폰트 (맑은 고딕 또는 사용자 지정 폰트)
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, font_size)
            else:
                # 윈도우 C:/Windows/Fonts 내 기본 폰트 하드코딩 백업
                default_font = "C:/Windows/Fonts/malgun.ttf"
                font = ImageFont.truetype(default_font, font_size)
        except OSError:
            # 기본 폰트조차 로드 실패 시
            font = ImageFont.load_default()
            
        # 1. 텍스트 자동 줄바꿈 (Word Wrap)
        # 박스를 넘치지 않도록 글자를 자름
        wrapped_lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            # getsize() deprecated -> getbbox() 사용
            if font.getbbox(test_line)[2] <= box_width * 0.9: # 10% 양옆 여유 마진
                current_line = test_line
            else:
                if current_line:
                    wrapped_lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            wrapped_lines.append(current_line.strip())
            
        # 2. 줄바꿈된 전체 텍스트들의 총 높이 계산
        total_text_height = sum([font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_lines])
        
        # 3. 중앙 정렬 시작 기준점
        current_y = min_y + (box_height - total_text_height) / 2
        
        # 4. 각 줄을 가운데 정렬로 그리기
        for line in wrapped_lines:
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            line_height = bbox[3] - bbox[1]
            
            x_pos = min_x + (box_width - line_width) / 2
            
            # 검은색 텍스트(만화 기본), 약간의 가독성을 위한 하얀색 테두리(Stroke) 추가
            draw.text((x_pos, current_y), line, fill=(0, 0, 0), font=font,
                      stroke_width=2, stroke_fill=(255, 255, 255))
            current_y += line_height + 4 # 줄간격 약간의 여백 4픽셀

    print(f"[Typesetting 완료] 총 {len(translated_texts)}개의 텍스트를 이미지에 그렸습니다.")
    
    # 마지막으로 RGB -> BGR로 다시 전환하여 반환 
    final_cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return final_cv2_img

if __name__ == "__main__":
    pass
