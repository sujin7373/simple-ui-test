from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import time

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized") # 창 최대로 열기
# 스크립트 끝나고 브라우저 열리게 하기 - True
# 스크립트 끝나고 브라우저 닫히게 하기 - False
chrome_options.add_experimental_option("detach", True)

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10) # 요소가 바로 안 나타나도 최대 10초까지 재시도하며 기다려


# 회원가입 페이지로 이동
driver.get("http://localhost:5000/signup")
time.sleep(3)
print("페이지 이동 완료")

try :
    # 요소 찾고 입력
    driver.find_element(By.ID, "username").send_keys("adadad")
    driver.find_element(By.ID, "password").send_keys("soojin0703")
    driver.find_element(By.ID, "confirmPassword").send_keys("soojin0703")

    # 회원가입 하기 버튼 클릭
    driver.find_element(By.XPATH, '//button[@type = "submit"]').click()

    time.sleep(3)
    
    # if-else 제대로 쓰기 위해서 find_element가 아닌 elements 사용
    # 'elements는 요소를 찾지 못해도 빈 리스트를 반환한다' 는 것을 활용
    already_text = driver.find_elements(By.XPATH, "//div[contains(text(), 'already')]")

    if already_text :
        # already_text가 빈 리스트가 아닐때 (중복 계정이 존재할 때)
        print("회원가입 실패 - 중복 계정 존재")
    else :
        # already_text가 빈 리스트일 때 (로그인 성공했을 때)
        username = driver.find_element(By.XPATH, "//span[@data-testid = 'text-welcome-username']")
        print(f"회원가입 성공! 유저 이름 : {username.text}")
    
except NoSuchElementException :
    # 중복 메세지도 없고 성공 요소도 안 나타난 경우
    print("회원가입 실패")
    
cookies = driver.get_cookies()

if not cookies :
    print("쿠키가 비어 있습니다")
    
else :
    cookies_path = os.path.join("tests/exam", "cookies.json")
    with open(cookies_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii = False, indent = 2)
        print("쿠키가 JSON 파일로 저장되었습니다.")
    

