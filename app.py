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

    # ✅ 검색 기능 추가 (차량명 검색)
    if search_query:
        query = "SELECT * FROM auction_cars WHERE 차명 LIKE %s"
        cursor.execute(query, (f"%{search_query}%",))
    else:
        query = "SELECT * FROM auction_cars"
        cursor.execute(query)

    cars = cursor.fetchall()
    conn.close()

    formatted_cars = []
    for car in cars:
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
        })
    for index, car in enumerate(formatted_cars, start=1):
        car["순서 ID"] = index  

    return render_template("index.html", cars=formatted_cars, search_query=search_query)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
