from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
import bcrypt
import uuid

app = FastAPI()

# ✅ 데이터베이스 연결
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# ✅ 회원 테이블에 "사용자ID" 필드 추가
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    사용자ID TEXT UNIQUE,
    이름 TEXT,
    주민등록번호 TEXT UNIQUE,
    전화번호 TEXT,
    비밀번호 TEXT,
    정보제공동의 BOOLEAN
)
""")

# ✅ 세션 테이블 추가 (중복 로그인 방지)
cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    사용자ID TEXT PRIMARY KEY,
    세션ID TEXT
)
""")
conn.commit()

# ✅ 회원가입 요청 모델 (사용자 ID 추가)
class 회원가입요청(BaseModel):
    사용자ID: str  # 사용자가 설정하는 로그인 ID
    이름: str
    주민등록번호: str
    전화번호: str
    비밀번호: str
    정보제공동의: bool

# ✅ 로그인 요청 모델
class 로그인요청(BaseModel):
    사용자ID: str
    비밀번호: str

# ✅ 비밀번호 해싱 함수
def 해시_비밀번호(비밀번호: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(비밀번호.encode('utf-8'), salt).decode('utf-8')

# ✅ 회원가입 API (사용자 ID 추가)
@app.post("/회원가입", summary="회원가입 요청", description="새로운 사용자를 등록합니다.")
def 회원가입(사용자: 회원가입요청):
    if not 사용자.정보제공동의:
        raise HTTPException(status_code=400, detail="📢 정보 제공에 동의해야 가입할 수 있습니다.")

    cursor.execute("SELECT * FROM users WHERE 사용자ID=? OR 주민등록번호=?", (사용자.사용자ID, 사용자.주민등록번호))
    기존_사용자 = cursor.fetchone()
    
    if 기존_사용자:
        raise HTTPException(status_code=400, detail="🚨 이미 존재하는 사용자 ID 또는 주민등록번호입니다.")

    해시된_비밀번호 = 해시_비밀번호(사용자.비밀번호)

    cursor.execute("""
    INSERT INTO users (사용자ID, 이름, 주민등록번호, 전화번호, 비밀번호, 정보제공동의)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (사용자.사용자ID, 사용자.이름, 사용자.주민등록번호, 사용자.전화번호, 해시된_비밀번호, 사용자.정보제공동의))
    
    conn.commit()
    
    return {"메시지": "🎉 회원가입이 완료되었습니다!", "사용자ID": 사용자.사용자ID}

# ✅ 로그인 API
@app.post("/로그인", summary="로그인 요청", description="사용자 ID와 비밀번호로 로그인합니다.")
def 로그인(요청: 로그인요청):
    cursor.execute("SELECT 사용자ID, 비밀번호 FROM users WHERE 사용자ID = ?", (요청.사용자ID,))
    사용자 = cursor.fetchone()
    
    if not 사용자 or not bcrypt.checkpw(요청.비밀번호.encode(), 사용자[1].encode()):
        raise HTTPException(status_code=401, detail="🚨 사용자 ID 또는 비밀번호가 틀렸습니다.")
    
    # ✅ 기존 세션 삭제 (중복 로그인 방지)
    cursor.execute("DELETE FROM sessions WHERE 사용자ID = ?", (요청.사용자ID,))
    
    # ✅ 새로운 세션 생성
    세션ID = str(uuid.uuid4())  # 랜덤 세션 ID 생성
    cursor.execute("INSERT INTO sessions (사용자ID, 세션ID) VALUES (?, ?)", (요청.사용자ID, 세션ID))
    
    conn.commit()
    
    return {"메시지": "✅ 로그인 성공", "세션ID": 세션ID}

# ✅ 로그아웃 API
@app.post("/로그아웃", summary="로그아웃 요청", description="사용자의 세션을 삭제하여 로그아웃합니다.")
def 로그아웃(사용자ID: str):
    cursor.execute("DELETE FROM sessions WHERE 사용자ID = ?", (사용자ID,))
    conn.commit()
    return {"메시지": "👋 로그아웃 완료"}