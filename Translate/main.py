import os
import sys

# 프로젝트의 핵심 모듈 1~4단계 불러오기
from step1_detector import detect_text_boxes
from step2_vlm_translator import translate_boxes
from step3_inpainting import inpaint_image
from step4_typesetting import typeset_image

def process_single_image(img_path: str):
    """지정된 이미지를 V3 원리(나노 바나나 하이브리드)에 따라 4단계로 변환합니다."""
    
    # 1. 텍스트 스파팅 (Spotting)
    bboxes = detect_text_boxes(img_path)
    if not bboxes:
        print(f"-> 스킵: '{os.path.basename(img_path)}' 에서 텍스트를 찾지 못했습니다.")
        return False
        
    print(f"-> 1단계 완료: {len(bboxes)}개의 말풍선을 탐지했습니다.")

    # 2. VLM 크롭 번역 (Translation)
    translated_data = translate_boxes(img_path, bboxes)
    if not translated_data:
        print(f"-> 스킵: 번역된 데이터가 없습니다.")
        return False
        
    print("-> 2단계 완료: 제미니 문맥 번역 완료 (난수 수면 적용)")

    # 3. 배경 복원 (Inpainting)
    inpainted_path = inpaint_image(img_path, translated_data)
    if not inpainted_path or not os.path.exists(inpainted_path):
        print(f"-> 에러: 식질 생성 실패.")
        return False
        
    print("-> 3단계 완료: 무손실 배경 복원 완료")

    # 4. 동적 조판 (Typesetting)
    final_path = typeset_image(inpainted_path, translated_data, output_path=img_path.replace('.jpg', '_translated.jpg').replace('.png', '_translated.png'))
    
    if final_path and os.path.exists(final_path):
        # 성공 후 임시 식질 파일(cleaned) 삭제로 디렉토리 최적화
        try:
            os.remove(inpainted_path)
        except Exception:
            pass
        print(f"★ 파이프라인 최종 완료: {final_path}")
        return True
    return False

def main():
    print("="*60)
    print(" 안티그래비티 일본 만화 자동 번역 파이프라인 V3")
    print(" (PaddleOCR 탐지 + Gemini 비전 번역 하이브리드)")
    print("="*60)
    
    # 만약 test_images 폴더를 인자로 주거나 기본 지정 시 (명령어: python main.py test_images)
    target_folder = "test_images" if len(sys.argv) < 2 else sys.argv[1]
    
    if not os.path.isdir(target_folder):
        print(f"오류: 존재하지 않는 폴더입니다. => {target_folder}")
        sys.exit(1)
        
    image_files = [f for f in os.listdir(target_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.lower().endswith('_translated.jpg') and not f.lower().endswith('_translated.png')]
    filter_files = [f for f in image_files if "debug" not in f.lower() and "translated" not in f.lower()]
    
    if not filter_files:
        print(f"'{target_folder}' 폴더에 변환할 원본 이미지 파일이 없습니다.")
        sys.exit(0)
        
    print(f"\n총 {len(filter_files)}장의 원본 이미지 처리를 시작합니다...")
    
    success_count = 0
    for idx, filename in enumerate(filter_files):
        img_path = os.path.join(target_folder, filename)
        print(f"\n[{idx+1}/{len(filter_files)}] 프로세스 시작: {filename}")
        
        try:
            if process_single_image(img_path):
                success_count += 1
        except Exception as e:
            print(f"❌ '{filename}' 처리 중 치명적 오류 발생: {e}")
            
    print("="*60)
    print(f"모든 작업이 종료되었습니다. (성공: {success_count} / 전체: {len(filter_files)})")
    print("="*60)

if __name__ == "__main__":
    main()
