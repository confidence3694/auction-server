
from flask import Flask

app = Flask(__name__)


from flask import Flask, render_template, request
import pymysql
import os

app = Flask(__name__)

# ✅ MySQL 연결 함수
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),  # 기본값: 로컬 MySQL 서버
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", "ss770528!!"),
        database=os.getenv("DB_NAME", "auction_db"),
        cursorclass=pymysql.cursors.DictCursor
    )

# ✅ 기본 홈 화면

@app.route("/")
def home():
    return index()  # 기본 페이지에서도 검색 화면 보이도록 수정

# 기존 코드 그대로 유지!


from flask import Flask, render_template, request
import pymysql
import re  

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="ss770528!!",  
        database="auction_db",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4"
    )

@app.route('/')
def index():
    search_query = request.args.get('search', '').strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT 차명, 연식, 주행거리, 최저매각가격, 연료종류, 매각기일, 사건번호, 물건번호, 등록번호, 담당
        FROM auction_cars
        WHERE 차명 LIKE %s
        ORDER BY 매각기일
    """ if search_query else """
        SELECT 차명, 연식, 주행거리, 최저매각가격, 연료종류, 매각기일, 사건번호, 물건번호, 등록번호, 담당
        FROM auction_cars
        ORDER BY 매각기일
    """

    cursor.execute(query, (f"%{search_query}%",) if search_query else ())
    cars = cursor.fetchall()
    conn.close()

    formatted_cars = []
    for car in cars:
<<<<<<< HEAD
        mileage = re.sub(r'[^0-9]', '', car["주행거리"]) if car["주행거리"] else "0"
        price = re.sub(r'[^0-9]', '', car["최저매각가격"]) if car["최저매각가격"] else "0"

        formatted_cars.append({
            "경매 ID": car["id"],  
            "차량명": car["차명"],  
            "연식": car["연식"] + "년",
            "주행거리": f'{int(mileage):,} km' if mileage else "정보 없음",
            "최저 매각 가격": f'{int(price):,} 원' if price else "정보 없음",
            "연료 종류": car["연료종류"],  
            "매각 기일": car["매각기일"],  
            "사건 번호": car["사건번호"],  
            "물건 번호": car["물건번호"]  
=======
        # ✅ 기존 코드 유지 (수정 전)
        try:
            distance = car["주행거리"].replace(",", "").replace("km", "").replace("KM", "").strip()
            distance = int(float(distance))  # float 변환 후 int 처리
            formatted_distance = f"{distance:,} km"
        except (ValueError, TypeError):
            formatted_distance = "정보 없음"
        
        formatted_cars.append({
            "차명": car["차명"] if car["차명"] else "이름 없음",
            "연식": f'{car["연식"]}년' if car["연식"] else "정보 없음",
            # ✅ 수정된 부분 적용 (주행거리 예외 처리 포함)
            "주행거리": formatted_distance,
            "최저매각가격": f'{int(car["최저매각가격"].replace(",", "").replace("원", "").strip()):,.0f}원'
                               if car["최저매각가격"] and car["최저매각가격"] != "정보 없음" else "정보 없음",     
            "연료종류": car["연료종류"] if car["연료종류"] else "정보 없음",
            "매각기일": car["매각기일"] if car["매각기일"] else "정보 없음",
            "사건번호": car["사건번호"] if car["사건번호"] else "정보 없음",
            "물건번호": car["물건번호"] if car["물건번호"] else "정보 없음",
            "등록번호": car["등록번호"] if car["등록번호"] else "정보 없음",
            "담당": car["담당"] if car["담당"] else "정보 없음",
            "경매_URL": "https://www.courtauction.go.kr/pgj/index.on?w2xPath=/pgj/ui/pgj100/PGJ151F00.xml"
>>>>>>> e81bf37 (Save changes before pulling)
        })

    for index, car in enumerate(formatted_cars, start=1):
        car["순서 ID"] = index

    return render_template("index.html", cars=formatted_cars, search_query=search_query)

# +++++++++ 🔧 `info` (차량 상세 정보 추가) +++++++++
@app.route("/info/<int:car_id>")
def info(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM auction_cars WHERE id = %s
    """
    cursor.execute(query, (car_id,))
    car_info = cursor.fetchone()
    conn.close()

    if not car_info:
        return "차량 정보를 찾을 수 없습니다.", 404

    return render_template("info.html", car=car_info)

# ✅ 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
