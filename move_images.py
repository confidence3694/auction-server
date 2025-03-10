import os
import shutil

# ✅ 현재 프로젝트 폴더 (경매웹사이트)
project_dir = r"C:\Users\user\Desktop\경매웹사이트"

# ✅ 이미지가 저장된 폴더 (현재 프로젝트 폴더 안에서 검색)
image_source_folder = project_dir  # 이미지가 어디 있는지 정확히 모를 경우 프로젝트 폴더 전체 검색

# ✅ 이미지가 이동할 폴더 (static/images/)
target_folder = os.path.join(project_dir, "static", "images")

# ✅ 대상 폴더 없으면 생성
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# ✅ 이미지 파일 이동
moved_files = []
for root, _, files in os.walk(image_source_folder):
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg"):  # PNG, JPG 파일만 이동
            source_path = os.path.join(root, file)
            target_path = os.path.join(target_folder, file)
            if not os.path.exists(target_path):  # 중복 방지
                shutil.move(source_path, target_path)
                moved_files.append(file)

# ✅ 이동 결과 출력
if moved_files:
    print("📂 이미지 파일이 static/images/ 폴더로 이동 완료!")
    for f in moved_files:
        print(f" - {f}")
else:
    print("⚠️ 이동할 이미지 파일이 없습니다!")
