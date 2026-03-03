import base64
import requests
import os

def test_cloud_vision(image_path, api_key):
    """Google Cloud Vision API가 현재 발급된 API 키로 동작하는지 검증"""
    print(f"\n--- [1] Cloud Vision API(GEMINI_API_KEY) 호환 테스트 ---")
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [
            {
                "image": {"content": encoded_string},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
            }
        ]
    }

    try:
        response = requests.post(url, json=payload)
        res_json = response.json()
        
        if "error" in res_json:
            print(f"❌ Cloud Vision API 접근 거부 (Generative AI 전용 키일 가능성 높음):\n{res_json['error']['message']}")
            return False
        else:
            print("✅ Cloud Vision API 연동 성공! 이 방식을 채택합니다.")
            return True
            
    except Exception as e:
        print(f"❌ 요청 오류: {e}")
        return False

if __name__ == "__main__":
    img_path = "test_images/Gallery_Fake_33_003.jpg"
    api_key = "AIzaSyACj_8hNqYaZkTbQKAZ0RDgyP1DriLYkUA"
    
    is_vision_ok = test_cloud_vision(img_path, api_key)
    
    if not is_vision_ok:
        print("\n--- [2] 대안: PaddleOCR 탐지기 도입 진행 권고 ---")
        print("-> Generative AI 키로는 Vision API 접근이 불가능합니다.")
        print("-> pip install paddlepaddle paddleocr 을 통해 오프라인 최고 성능 스파팅 라이브러리를 구축해야 합니다.")
