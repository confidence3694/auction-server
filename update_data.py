import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Google Sheets API 인증 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# ✅ Google 스프레드시트 열기
spreadsheet = client.open("경매 차량 데이터")  # 본인의 Google Sheets 문서 이름으로 변경!
sheet = spreadsheet.sheet1  # 첫 번째 시트 선택

# ✅ 크롤링한 데이터 (예제 데이터)
new_data = [
    ["Kia Sorento", "2022", "디젤", "202500140", "28000000", "2025-04-10"],
    ["Hyundai Tucson", "2023", "가솔린", "202500141", "26000000", "2025-04-12"]
]

# ✅ 중복 확인 후 추가하는 함수
def add_new_data(data):
    existing_data = sheet.get_all_values()  # 현재 저장된 데이터 가져오기
    existing_case_numbers = {row[3] for row in existing_data}  # 사건번호(고유값) 가져오기

    for row in data:
        if row[3] not in existing_case_numbers:  # 사건번호가 없으면 추가
            sheet.append_row(row)
            print(f"✅ 새 데이터 추가됨: {row}")

# ✅ 실행
add_new_data(new_data)
print("🚀 크롤링 데이터 업데이트 완료!")
import schedule
import time
import os

def run_update_script():
    print("🚀 크롤링 데이터 자동 업데이트 실행 중...")
    os.system("python update_data.py")

# ✅ 매일 오전 9시 실행
schedule.every().day.at("09:00").do(run_update_script)

print("⏳ 자동 스케줄러 실행 중... (Ctrl+C로 종료)")

while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 체크
