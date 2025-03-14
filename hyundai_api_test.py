import requests
import certifi

# ✅ 1. 현대자동차 API 인증 정보
CLIENT_ID = "87c4ddff-a2eb-4df5-b582-af0162aae1d4"
CLIENT_SECRET = "MKyx0rMRlby9iHXkvCJJuKgL6rJYhi4nxQVs0HcVvSMc9Y3k"

# ✅ 2. Access Token 발급
def get_access_token():
    url = "https://api.hyundai.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(url, headers=headers, data=data, verify=certifi.where())  # ✅ 인증서 적용
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("✅ Access Token 발급 완료:", access_token)
        return access_token
    else:
        print("❌ Access Token 발급 실패:", response.text)
        return None

# ✅ 3. 차량 등록번호로 제원 조회
def get_car_specs(registration_number, access_token):
    url = f"https://api.hyundai.com/v1/car/specs?reg_no={registration_number}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, verify=certifi.where())  # ✅ 인증서 적용

    if response.status_code == 200:
        data = response.json()
        print("✅ 차량 제원 정보:")
        print(f"🚗 모델명: {data.get('modelName', '정보 없음')}")
        print(f"⚙ 배기량: {data.get('engineSize', '정보 없음')}cc")
        print(f"⛽ 연료: {data.get('fuelType', '정보 없음')}")
        print(f"🛠 변속기: {data.get('transmission', '정보 없음')}")
    else:
        print("❌ 차량 정보를 불러오지 못했습니다:", response.text)

# ✅ 4. 실행 코드
if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        car_number = input("🚗 조회할 차량 등록번호를 입력하세요 (예: 12가1234): ")
        get_car_specs(car_number, access_token)
