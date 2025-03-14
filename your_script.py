import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service  # ✅ 크롬 드라이버 실행용


# ✅ 크롬 드라이버 실행 함수
def setup_driver():
    """📌 크롬 드라이버 실행 및 설정"""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("detach", True)

    chromedriver_path = "C:/Users/user/OneDrive/바탕 화면/auction_crawler/chromedriver.exe"  # ✅ 크롬 드라이버 절대 경로
    
    try:
        service = Service(chromedriver_path)  # ✅ 크롬 드라이버 경로 지정
        driver = webdriver.Chrome(service=service, options=options)
        return driver  # ✅ 실행된 드라이버 반환
    except Exception as e:
        print(f"❌ 크롬 드라이버 실행 오류: {e}")
        return None  # ❌ 오류 발생 시 None 반환






def extract_data_from_page(driver, row_index):
    """📌 상세 페이지에서 데이터 + 물건번호 추출"""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        fields = {
            "차명": "차명",
            "연식": "연식",
            "주행거리": "주행거리",
            "최저매각가격": "최저매각가격",
            "연료종류": "연료종류",
            "매각기일": "매각기일",
            "사건번호": "사건번호"
        }

        data = {}
        for key, title in fields.items():
            try:
                xpath = f"//td[@data-title='{title}']"
                element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
                data[key] = element.text.strip()
            except (TimeoutException, NoSuchElementException):
                data[key] = "N/A"

        # ✅ 물건번호 크롤링 수정
        try:
            물건번호_xpath = "//td[@data-title='물건번호']/span"
            물건번호_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 물건번호_xpath))
            )
            data["물건번호"] = 물건번호_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            data["물건번호"] = "N/A"

        try:
            등록번호_xpath = "//*[@id='mf_wfm_mainFrame_gen_carGdsDts_0_spn_carRegNo']"
            등록번호_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 등록번호_xpath))
            )
            data["등록번호"] = 등록번호_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            data["등록번호"] = "N/A"

        try:
            담당_xpath = "//*[@id='mf_wfm_mainFrame_spn_gdsDtlSrchCortNm']"
            담당_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 담당_xpath))
            )
            data["담당"] = 담당_element.text.strip()
        except (TimeoutException, NoSuchElementException):
            data["담당"] = "N/A"

  

        print(f"✅ 데이터 수집 완료: {data}")
        return data

    except Exception as e:
        print(f"❌ 데이터 수집 실패: {e}")
        return None





def click_next_page(driver, current_page):
    """📌 다음 페이지 버튼 클릭 (웹사이트 구조에 맞게 수정)"""
    try:
        # 10페이지마다 페이지 그룹이 바뀌는 경우 처리
        if current_page % 10 == 0:  # 10, 20, 30 페이지일 경우
            print(f"➡️ {current_page}페이지에서 다음 버튼 찾는 중...")
            
            # CSS 선택자로 '다음' 버튼 시도 (더 안정적인 경우가 많음)
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.w2pageList_col_next"))
                )
                print("CSS 선택자로 '다음' 버튼 찾음")
                next_button.click()  # JavaScript 대신 직접 클릭
                time.sleep(5)  # 페이지 로딩 대기 시간 충분히 제공
                print("➡️ '다음' 버튼 클릭 완료")
                return True
            except Exception as e:
                print(f"CSS 선택자로 버튼 찾기 실패: {str(e)}")
                
                # XPath로 시도
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'w2pageList_col_next')]"))
                    )
                    print("XPath로 '다음' 버튼 찾음")
                    # JavaScript로 클릭 시도
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(5)
                    print("➡️ '다음' 버튼 JavaScript로 클릭 완료")
                    return True
                except Exception as e2:
                    print(f"XPath로 버튼 찾기 실패: {str(e2)}")
                    
                    # 마지막 시도: ID로 찾기
                    try:
                        next_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='mf_wfm_mainFrame_pgl_gdsDtlSrchPage_next_btn']/button"))
                        )
                        print("ID로 '다음' 버튼 찾음")
                        # JavaScript로 클릭 강제 실행
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", next_button)
                        time.sleep(5)
                        print("➡️ '다음' 버튼 ID로 클릭 완료")
                        return True
                    except Exception as e3:
                        print(f"모든 방법으로 '다음' 버튼 찾기 실패: {str(e3)}")
                        return False
        else:
            # 일반 페이지는 숫자로 직접 이동
            next_page_num = current_page + 1
            print(f"➡️ {next_page_num}페이지 버튼 찾는 중...")
            
            next_page_xpath = f"//*[@id='mf_wfm_mainFrame_pgl_gdsDtlSrchPage_page_{next_page_num}']"
            try:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, next_page_xpath))
                )
                # 스크롤하여 버튼이 보이게 함
                driver.execute_script("arguments[0].scrollIntoView(true);", next_page_button)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", next_page_button)
                time.sleep(3)
                print(f"➡️ {next_page_num}페이지로 이동 완료")
                return True
            except Exception as e:
                print(f"❌ {next_page_num}페이지 버튼을 찾을 수 없음: {str(e)}")
                return False
                
    except Exception as e:
        print(f"❌ 페이지 이동 중 예상치 못한 오류 발생: {str(e)}")
        return False

def search_auction_items(driver):
    """📌 경매 물건 검색 조건 선택"""
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "경매물건"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "물건상세검색"))).click()

    law_court_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mf_wfm_mainFrame_sbx_rletCortOfc"]'))
    ))
    law_court_select.select_by_index(0)  
    print("✅ 법원 선택 완료!")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[text()='차량및운송장비']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[text()='차량']"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//option[text()='승용차']"))).click()

    search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "mf_wfm_mainFrame_btn_gdsDtlSrch"))
    )
    search_button.click()
    time.sleep(5)
    print("✅ 검색 완료!")

import pymysql
from datetime import datetime



def delete_old_auctions():
    """📌 MySQL에서 경매가 지난 데이터 자동 삭제"""
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="ss770528!!",
            database="auction_db",
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4"
        )
        cursor = conn.cursor()

        # ✅ 현재 날짜보다 경매 기일이 지난 데이터 삭제
        delete_query = "DELETE FROM auction_cars WHERE STR_TO_DATE(LEFT(매각기일, 16), '%Y.%m.%d %H:%i') < NOW();"
        cursor.execute(delete_query)
        conn.commit()
        print("✅ MySQL에서 지난 경매 데이터 삭제 완료!")

    except Exception as e:
        print(f"❌ MySQL 데이터 삭제 오류: {e}")

    finally:
        cursor.close()
        conn.close()





# ✅ MySQL 연결 함수
def connect_mysql():
    """📌 Cloud SQL 연결"""
    return pymysql.connect(
        host="34.64.140.69",  # ✅ Cloud SQL 공개 IP
        user="root",  # ✅ 사용자명
        password="ss770528!!",  # ✅ 비밀번호 (본인 설정값 입력)
        database="auction_db",
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4"
    )

def save_to_mysql(data):
    """📌 크롤링한 데이터를 MySQL auction_cars 테이블에 저장"""
    conn = None  # 🔹 conn을 미리 선언하여 오류 방지
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="ss770528!!",
            database="auction_db",
            cursorclass=pymysql.cursors.DictCursor,
            charset="utf8mb4"  # 🔹 UTF-8 설정
        )
        cursor = conn.cursor()

        # ✅ MySQL INSERT 쿼리 (중복 시 최저매각가격 업데이트)
        query = """
        INSERT INTO auction_cars (차명, 연식, 주행거리, 최저매각가격, 연료종류, 매각기일, 사건번호, 물건번호, 담당, 등록번호)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 최저매각가격 = VALUES(최저매각가격);
        """

        # ✅ 데이터 UTF-8 변환 적용
        car_data = tuple(
            str(data.get(key, "N/A")).encode("utf-8", "ignore").decode("utf-8") for key in
            ["차명", "연식", "주행거리", "최저매각가격", "연료종류", "매각기일", "사건번호", "물건번호", "담당", "등록번호"]
        )

        # ✅ 데이터 삽입 실행
        cursor.execute(query, car_data)
        conn.commit()

        print(f"✅ MySQL 저장 완료: {car_data}")

    except Exception as e:
        print(f"❌ MySQL 저장 오류: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()






def click_all_usage_locations(driver):
    """📌 모든 페이지의 차량 크롤링"""
    total_processed = 0
    page = 1

    while True:
        print(f"📌 페이지 {page} 크롤링 시작...")

        try:
            usage_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), '사용본거지')]"))
            )
            print(f"🔎 발견된 차량 개수: {len(usage_links)} (페이지 {page})")

            for i in range(len(usage_links)):  # ✅ i는 현재 차량의 순서 (row_index로 사용)
                try:
                    usage_links = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), '사용본거지')]"))
                    )
                    driver.execute_script("arguments[0].click();", usage_links[i])
                    print(f"✅ 차량 {i+1} 상세 페이지 이동 (페이지 {page})")
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    data = extract_data_from_page(driver, i)  # ✅ row_index(i)를 추가하여 오류 해결!
                    if data:
                        total_processed += 1
                        
                        save_to_mysql(data)

                    back_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[@id='mf_wfm_mainFrame_trigger1']"))
                    )
                    driver.execute_script("arguments[0].click();", back_button)

                except Exception as e:
                    print(f"❌ 차량 크롤링 중 오류: {e}")

            if not click_next_page(driver, page):
                break
            page += 1  

        except Exception as e:
            print(f"❌ 페이지 크롤링 중 오류: {e}")
            break

    print(f"✅ 총 크롤링된 차량 수: {total_processed}")

def main():
    """📌 메인 실행 함수"""
    driver = setup_driver()

    if driver is None:
        print("❌ 드라이버 실행 실패. 프로그램 종료.")
        return  

    all_cars = []  # ✅ 크롤링한 데이터를 저장할 리스트

    try:
        driver.get("https://www.courtauction.go.kr/")
        search_auction_items(driver)
        
        total_processed = 0
        page = 1

        while True:  # ✅ 🔵 제한 없이 크롤링
            print(f"📌 페이지 {page} 크롤링 시작...")

            try:
                usage_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), '사용본거지')]"))
                )
                print(f"🔎 발견된 차량 개수: {len(usage_links)} (페이지 {page})")

                for i in range(len(usage_links)):  
                    try:
                        usage_links = WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), '사용본거지')]"))
                        )
                        driver.execute_script("arguments[0].click();", usage_links[i])
                        print(f"✅ 차량 {i+1} 상세 페이지 이동 (페이지 {page})")
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                        data = extract_data_from_page(driver, i)
                        if data:
                            total_processed += 1
                            all_cars.append(data)  # ✅ 크롤링한 데이터를 리스트에 추가
                            
                            save_to_mysql(data)

                        back_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, "//*[@id='mf_wfm_mainFrame_trigger1']"))
                        )
                        driver.execute_script("arguments[0].click();", back_button)

                    except Exception as e:
                        print(f"❌ 차량 크롤링 중 오류: {e}")

                if not click_next_page(driver, page):  # ✅ 다음 페이지가 없으면 종료
                    break
                page += 1  

            except Exception as e:
                print(f"❌ 페이지 크롤링 중 오류: {e}")
                break

        print(f"✅ 총 크롤링된 차량 수: {total_processed}")

    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")

    finally:
        input("✔ 크롤링 완료! 브라우저 닫으려면 엔터...")
        driver.quit()


if __name__ == "__main__":
    delete_old_auctions()  # ✅ 크롤링 전에 지난 데이터 삭제!
    main()  # ✅ 크롤링 실행 (한 번만 실행)

