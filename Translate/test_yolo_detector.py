from huggingface_hub import hf_hub_download, list_repo_files
from ultralytics import YOLO
import cv2

repo_id = "ogkalu/comic-text-segmenter-yolov8m"
print(f"HuggingFace에서 {repo_id} 분석 중...")

# Repo 내의 .pt 모델 파일명 탐색
files = list_repo_files(repo_id)
pt_files = [f for f in files if f.endswith('.pt')]

if not pt_files:
    print("에러: .pt 모델 파일을 찾을 수 없습니다.")
    exit(1)

model_filename = pt_files[0]
print(f"모델 파일 발견: {model_filename}")
print("모델 다운로드 / 로딩 중 (최초 1회만 다운로드됩니다)...")

# 모델 다운로드 및 로드
model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
model = YOLO(model_path)

# 이미지 예측
test_img = "test_images/Gallery_Fake_33_003.jpg"
print(f"이미지 예측 시작: {test_img}")
results = model(test_img)

# 결과물에서 바운딩 박스 추출
boxes = results[0].boxes.xyxy.cpu().numpy()
print(f"\n✅ 완료: 총 {len(boxes)}개의 텍스트(말풍선) 영역을 탐지했습니다!")

# 원본 이미지에 빨간색 박스 렌더링
img = cv2.imread(test_img)
for idx, box in enumerate(boxes):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
    cv2.putText(img, str(idx+1), (x1, max(y1-10, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

save_path = "debug_yolo_boxes.jpg"
cv2.imwrite(save_path, img)
print(f"결과 이미지 저장 완료: {save_path}")
