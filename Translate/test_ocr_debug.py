import sys
from step1_ocr import detect_and_extract_text

if __name__ == "__main__":
    test_img = "test_images/Gallery_Fake_33_003.jpg"
    with open("ocr_debug_log.txt", "w", encoding="utf-8") as f:
        f.write(f"--- 디버깅 테스트 시작: {test_img} ---\n")
        results = detect_and_extract_text(test_img, lang_list=['ja'])
        
        if not results:
            f.write("결과: 반환된 박스가 0개입니다!! (EasyOCR이 아예 영역 자체를 못 잡고 있음)\n")
        else:
            f.write(f"결과: 총 {len(results)}개의 텍스트 박스 감지됨.\n")
            for idx, r in enumerate(results):
                f.write(f"[{idx+1}] Text: {r['text']}, Conf: {r['confidence']}, Box: {r['box']}\n")
