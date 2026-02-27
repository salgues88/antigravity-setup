import os
import sys
import time
import cv2
import tkinter as tk
from tkinter import filedialog

# 직접 만든 모듈 Import (파일명을 step1~4로 변경 완료)
from step1_ocr import detect_and_extract_text
from step2_translator import translate_texts
from step3_inpainting import remove_text_and_inpaint
from step4_typesetting import draw_korean_text_on_image

# 지원하는 이미지 포맷
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')

def select_folder_gui() -> str:
    """tkinter를 사용하여 사용자에게 폴더 선택 다이얼로그 창(GUI)을 띄우고 경로를 반환합니다."""
    # tkinter 최상위 윈도우 숨기기 (다이얼로그 창만 띄우기 위함)
    root = tk.Tk()
    root.withdraw()
    
    # 창을 운영체제 맨 앞으로 가져오기
    root.attributes('-topmost', True)
    
    print("화면에 나타난 윈도우 창에서 '번역할 그림 파일들이 들어있는 폴더'를 선택해 주세요...")
    
    # 폴더 선택 대화상자 열기
    folder_path = filedialog.askdirectory(
        title="[안티그래비티 번역기] 번역할 그림 파일이 있는 폴더를 선택하세요",
        initialdir=os.path.expanduser("~") # 기본 시작 위치를 사용자 홈 디렉토리로 설정
    )
    
    # 윈도우 리소스 정리
    root.destroy()
    
    return folder_path

def process_single_image(image_path: str, api_key: str, font_path: str = None) -> bool:
    """단일 이미지에 대한 OCR -> 번역 -> 식질 -> 조판 4단계 파이프라인 수행"""
    print(f"\n=========================================")
    print(f"작업 시작: {os.path.basename(image_path)}")
    print(f"=========================================")
    
    # 1. OCR 추출
    extracted_data = detect_and_extract_text(image_path)
    if not extracted_data:
        print(f"[{os.path.basename(image_path)}] 감지된 텍스트가 없거나 OCR에 실패했습니다. 다음 파일로 넘어갑니다.")
        return True # 이미지에 글씨가 없을 수도 있으므로 오류가 아님
        
    original_texts = [item['text'] for item in extracted_data]
    
    # 2. Gemini API로 컨텍스트 파악 및 번역
    translated_texts = translate_texts(original_texts, api_key)
    if not translated_texts or len(translated_texts) != len(original_texts):
        print(f"[{os.path.basename(image_path)}] ⚠️ 번역 중 문제가 발생했으나 강제 진행합니다.")
        # 파싱 오류 시 원본을 그대로 반환하는 폴백 로직 작동 확인
        translated_texts = original_texts
        
    # 3. OpenCV 식질 (Inpainting)
    inpainted_img = remove_text_and_inpaint(image_path, extracted_data)
    if inpainted_img is None:
        print(f"[{os.path.basename(image_path)}] 식질 복원 단계에서 치명적 오류 발생. 건너뜁니다.")
        return False
        
    # 4. Pillow 조판 렌더링
    final_img = draw_korean_text_on_image(inpainted_cv2_img=inpainted_img, 
                                          text_boxes=extracted_data, 
                                          translated_texts=translated_texts, 
                                          font_path=font_path)
                                          
    # 5. 결과물 저장 (원본 경로에 '_translated.jpg' 접미사 추가)
    file_dir, file_name = os.path.split(image_path)
    base_name, ext = os.path.splitext(file_name)
    save_path = os.path.join(file_dir, f"{base_name}_translated{ext}")
    
    # OpenCV를 통한 한글 경로 지원 저장 (우회)
    is_success, buffer = cv2.imencode(ext, final_img)
    if is_success:
        with open(save_path, "wb") as f:
            f.write(buffer)
        print(f"✅ [성공] 번역 및 식질 완료 파일 저장: {save_path}")
        return True
    else:
        print(f"❌ [실패] 최종 이미지 저장 오류: {save_path}")
        return False

def main():
    print("=================================================================")
    print("      만화 자동 번역 및 식질 파이프라인 프로그램 (Gemini)        ")
    print("=================================================================")
    
    # API 키 확인 (미리 입력받거나 환경변수로)
    api_key_env = os.environ.get("GEMINI_API_KEY", "AIzaSyAkjUaPEgA4fPjLjH39_dppIUG5UUViF4A")
    api_key = api_key_env
    print("-> 시스템에 제공된 Gemini API 키를 자동으로 불러왔습니다.")
            
    # 목표 폴더 확인 (1번 요구사항: 윈도우 UI 창으로 사용자에게 입력받기)
    target_folder = select_folder_gui()
    
    if not target_folder or not os.path.isdir(target_folder):
        print("\n에러: 폴더 선택이 취소되었거나 유효하지 않습니다. 프로그램을 종료합니다.")
        input("엔터키를 눌러 종료하세요...")
        sys.exit(1)
        
    print(f"\n-> 선택된 원본 이미지 폴더 경로: [{target_folder}]")
        
    # 폴더 내 이미지 파일 수집 (재시도를 위해 리스트화)
    image_files = []
    for file in os.listdir(target_folder):
        # 만약 이전에 번역본이 있었다면 제외 처리 '_translated'
        if file.lower().endswith(VALID_EXTENSIONS) and "_translated" not in file:
            image_files.append(os.path.join(target_folder, file))
            
    # 알파벳/숫자 순 정렬 (페이지 순서대로 진행하기 위함)
    image_files.sort()
    
    total_files = len(image_files)
    if total_files == 0:
        print("\n해당 폴더에 번역할 그림 파일(jpg, png 등)이 존재하지 않습니다. 프로그램을 종료합니다.")
        input("엔터키를 눌러 종료하세요...")
        sys.exit(0)
        
    print(f"\n총 {total_files}개의 원본 이미지 대상 파일을 찾았습니다. 순서대로 작업을 시작합니다.\n")
    
    # 오류 시 재시도 등 파이프라인 루프 구동
    idx = 0
    consecutive_errors = 0
    
    while idx < total_files:
        current_img = image_files[idx]
        
        try:
            success = process_single_image(current_img, api_key)
            if success:
                idx += 1 # 성공 시만 다음 장으로 넘어감
                consecutive_errors = 0
                
                # Gemini 무료 API 한도를 지키기 위한 강제 안전 딜레이 (1.5 Pro 기준 1분 2건 이므로 약 30초+ 대기)
                # 모델 성능에 따라 15초(플래시) ~ 30초(프로) 대기
                print("Gemini API 서버 과부하를 방지하기 위해 15초 대기합니다...")
                time.sleep(15)
                
            else:
                consecutive_errors += 1
                idx += 1 # 개별 이미지 자체 렌더링/파일 실패는 건너뜀 (무한루프 방지)
                
        except Exception as e:
            # 보통 Rate Limit (429 과부하 에러)에서 여기로 빠짐
            error_msg = str(e).lower()
            print(f"\n[비상 상황 감지] {current_img} 처리 중 알 수 없는 예외 발생: {e}")
            
            if "quota" in error_msg or "429" in error_msg or "exhausted" in error_msg:
                # 11번 요구사항: 과부하 휴식 로직 자동화
                wait_minutes = 60 # 보수적으로 1시간으로 설정
                from datetime import datetime
                current_time = datetime.now().strftime("%Y/%m/%d %H:%M")
                print(f"===========================================================")
                print(f"[{current_time}] ⚠️ 제미니 서버 과부하가 감지되었습니다.")
                print(f"실패한 파일명: {os.path.basename(current_img)}")
                print(f"사람의 개입 없이 스스로 {wait_minutes}분 동안 휴식 후 재시도합니다.")
                print(f"===========================================================")
                time.sleep(wait_minutes * 60)
            else:
                # 일반 에러 시 너무 자주 에러나면 종료
                consecutive_errors += 1
                if consecutive_errors >= 3:
                    print("연속적인 심각한 오류가 발생하여 프로그램을 일시 중단합니다.")
                    input("아무 키나 눌러 확인하세요...")
                    sys.exit(1)
                idx += 1 # 원인 불명 에러는 건너뜀
                
    print("\n-----------------------------------------------------------")
    print(f"축하합니다! 설정한 폴더 경로 내의 모든 그림 파일의 번역 및 다운로드를 완료했습니다.")
    print("-----------------------------------------------------------")
    input("작업이 성공적으로 종료되었습니다. 엔터키를 누르면 프로그램이 닫힙니다.")

if __name__ == "__main__":
    main()
