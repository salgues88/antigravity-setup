import google.generativeai as genai

# 테스트용 로컬 키 할당 (공개 저장소에는 커밋되지 않도록 추후 변경)
api_key = "AIzaSyACj_8hNqYaZkTbQKAZ0RDgyP1DriLYkUA"
genai.configure(api_key=api_key)

try:
    print("--- 사용 가능한 Gemini 모델 리스트 확인 ---")
    models = [m.name for m in genai.list_models() if 'gemini' in m.name]
    print(models)
    
    print("\n--- gemini-1.5-pro 모델 로딩 테스트 ---")
    model = genai.GenerativeModel('gemini-1.5-pro')
    print("gemini-1.5-pro 모델 초기화 성공!")
except Exception as e:
    print(f"오류 발생: {e}")
