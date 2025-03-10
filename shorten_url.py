import requests

# ✅ TinyURL API 키 설정
API_KEY = "eTa62bfCIFjYM3bAL8vahyJKq7uI81wBQjqiCNR3AewYBNS1mMOYUL7TaqNV"
TINYURL_API_URL = "https://api.tinyurl.com/create"

def shorten_url(long_url):
    """📌 긴 URL을 TinyURL로 단축하는 함수"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {"url": long_url}

    try:
        response = requests.post(TINYURL_API_URL, json=data, headers=headers)
        response_data = response.json()

        if "data" in response_data and "tiny_url" in response_data["data"]:
            return response_data["data"]["tiny_url"]  # ✅ 단축 URL 반환
        else:
            print(f"❌ URL 단축 실패: {response_data}")
            return None
    except Exception as e:
        print(f"❌ 요청 오류: {e}")
        return None

# ✅ 테스트 실행
if __name__ == "__main__":
    test_url = "https://example.com/very/long/image/url/that/needs/to/be/shortened"
    short_url = shorten_url(test_url)
    
    if short_url:
        print(f"✅ 단축된 URL: {short_url}")
    else:
        print("❌ URL 단축 실패")
