require('dotenv').config();
const express = require('express');
const mysql = require('mysql');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.set('view engine', 'ejs'); // EJS 템플릿 엔진 설정
app.use(express.static('public')); // 정적 파일 제공 (CSS 등)

// MySQL 연결 설정
const db = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASS || '',
    database: process.env.DB_NAME || 'auction_db'
});

// MySQL 연결 확인
db.connect(err => {
    if (err) {
        console.error('MySQL 연결 오류:', err);
        return;
    }
    console.log('MySQL 연결 성공');
});

// 경매 데이터 조회 API (JSON 들여쓰기 적용)
app.get('/api/cars', (req, res) => {
    const sql = 'SELECT * FROM auction_cars ORDER BY id DESC';
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify({ success: true, data: results }, null, 4));
    });
});

// 경매 차량 목록 웹 페이지 추가
app.get('/cars', (req, res) => {
    const sql = 'SELECT * FROM auction_cars ORDER BY id DESC';
    db.query(sql, (err, results) => {
        if (err) {
            return res.status(500).send('데이터를 불러오는 중 오류 발생');
        }
        res.render('cars', { cars: results });
    });
});

// 서버 실행
app.listen(PORT, () => {
    console.log(`서버 실행 중: http://localhost:${PORT}`);
    console.log(`차량 목록 페이지: http://localhost:${PORT}/cars`);
});