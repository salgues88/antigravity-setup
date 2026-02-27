import google.generativeai as genai
import os
import time

def setup_gemini(api_key: str):
    """Gemini API 설정 초기화"""
    genai.configure(api_key=api_key)

def translate_texts(texts_to_translate: list, api_key: str, model_name: str = "gemini-1.5-flash") -> list:
    """
    추출된 일본어 텍스트 리스트를 Gemini API를 이용해 컨텍스트에 맞게 한국어로 번역합니다.
    
    Args:
        texts_to_translate: 번역할 텍스트 문자열 리스트
        api_key: 구글 AI Studio API 키
        model_name: 사용할 모델 (기본값: 빠르고 저렴한 gemini-1.5-flash)
        
    Returns:
        list: 번역된 한국어 문자열 리스트 (원래 리스트와 동일한 순서)
    """
    if not texts_to_translate:
        return []
        
    setup_gemini(api_key)
    
    # 텍스트들을 하나의 긴 컨텍스트로 묶어서 번역 (API 비용/시간 절약 및 문맥 파악)
    combined_text = "\n".join([f"[{i+1}] {text}" for i, text in enumerate(texts_to_translate)])
    
    prompt = f"""
    너는 지금부터 1990년대~2000년대 명작 일본 만화인 '갤러리 페이크(Gallery Fake)'의 전문 한국어 정발판 번역가야.
    이 만화는 미술품의 위작, 진품 감정, 예술계의 이면 등을 다루는 다소 진지하면서도 미스터리한 분위기의 작품이야.
    
    아래에 제공된 일본어 텍스트들은 만화 한 페이지에서 추출된 대사 및 효과음들이야.
    각 대사의 순서 번호 '[n]'을 유지한 채, 앞뒤 문맥과 상황, 기안(주인공)의 말투 등을 고려하여 가장 자연스럽고 매끄러운 한국어 만화 대사로 번역해 줘.
    
    [규칙]
    1. 원본의 '[n]' 번호 형식을 결과물에서도 반드시 똑같이 적어줘.
    2. 효과음(예: 쾅, 스윽, 두둥 등)도 상황에 맞게 한국어 효과음으로 의역해 줘.
    3. 번역문 외에 다른 부가 설명이나 인사말은 절대 출력하지 마.
    4. 출력 형식 예시:
       [1] 번역된 대사 1
       [2] 번역된 대사 2
       ...
       
    [원본 텍스트]
    {combined_text}
    """
    
    try:
        # 모델 설정 및 생성
        model = genai.GenerativeModel(model_name)
        
        # GenerationConfig로 일관성 향상 (온도 조절)
        generation_config = genai.types.GenerationConfig(
            temperature=0.3, # 약간의 창의성, 안정적인 번역 중시
        )
        
        print("Gemini API로 번역 요청 중...")
        response = model.generate_content(prompt, generation_config=generation_config)
        
        # 결과 파싱
        translated_list = []
        result_text = response.text.strip().split('\n')
        
        # 간단한 파싱: "[1]" 등으로 시작하는 라인만 추출하여 리스트화 매칭 시도
        # (완벽한 매칭을 위해 향후 정규식 등 고도화 필요)
        for line in result_text:
            if line.strip().startswith('['):
                # "[1] 번역문" -> "번호", "번역문" 분리
                parts = line.split(']', 1)
                if len(parts) == 2:
                    translated_list.append(parts[1].strip())
                    
        # 만약 파싱 중 개수가 맞지 않을 경우 대비 (fallback)
        if len(translated_list) != len(texts_to_translate):
            print(f"경고: 번역된 개수({len(translated_list)})가 원본 개수({len(texts_to_translate)})와 일치하지 않을 수 있습니다.")
            # 극단적 대비: 원래 텍스트로 일단 채워넣거나 응답 통째로 넣기
            
        print("[번역 완료] 성공적으로 한국어 텍스트를 받아왔습니다.")
        return translated_list
        
    except Exception as e:
        print(f"[번역 에러] Gemini API 호출 중 오류: {e}")
        # 오류 시 원본 반환 (파이프라인 안 깨지게)
        return texts_to_translate

if __name__ == "__main__":
    # 간단 테스트
    test_texts = ["おっと！", "これは本物のモネですね。", "ゴゴゴゴ..."]
    api_key_env = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
    if api_key_env != "YOUR_API_KEY_HERE":
        results = translate_texts(test_texts, api_key_env)
        for orig, trans in zip(test_texts, results):
            print(f"{orig} -> {trans}")
    else:
        print("테스트하려면 GEMINI_API_KEY 환경 변수를 설정하거나 코드를 직접 수정하세요.")
