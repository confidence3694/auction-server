// Google Sheets 설정
const sheetId = "178cbMRtwkDaCm3xjLSeERMQ3cwIX--XeeD6FoQ8kaF8"; // 스프레드시트 ID
const sheetName = "cars_test"; // 시트 이름
const apiKey = "AIzaSyDX2FpQosfveKlDm43j840qXZT7kOcew1A"; // API 키

const url = `https://sheets.googleapis.com/v4/spreadsheets/${sheetId}/values/${sheetName}?key=${apiKey}`;

document.addEventListener("DOMContentLoaded", function() {
    const tableBody = document.querySelector("#carTableBody");
    
    if (!tableBody) {
        console.error("❌ 테이블을 찾을 수 없습니다. HTML에 id='carTableBody'가 있는지 확인하세요.");
        return;
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("✅ 데이터 확인:", data); // 데이터 출력
            if (!data.values) {
                console.error("❌ Google Sheets 데이터를 불러오지 못했습니다.");
                return;
            }

            const rows = data.values.slice(1); // 첫 번째 행(헤더) 제외
            rows.forEach(row => {
                let newRow = tableBody.insertRow();
                row.forEach(cell => {
                    let newCell = newRow.insertCell();
                    newCell.textContent = cell;
                });
            });
        })
        .catch(error => console.error("❌ 데이터 가져오기 오류:", error));
});
