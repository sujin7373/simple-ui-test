from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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

# WebDriverWait 쓰기 위한 초기 작업
wait = WebDriverWait(driver, 10)

# 회원가입 페이지로 이동
driver.get("http://localhost:5000/signup")
time.sleep(3)
print("페이지 이동 완료")

# 요소 찾고 입력
driver.find_element(By.ID, "username").send_keys("sdfsdf")
driver.find_element(By.ID, "password").send_keys("soojin0703")
driver.find_element(By.ID, "confirmPassword").send_keys("soojin0703")

# 회원가입 하기 버튼 클릭
driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    
try :
    # 중복 계정 에러 있을 때까지 기다리고 있으면 실패로 띄워줘
    error_already = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'already')]")))
    print("회원가입 실패 - 중복 계정 존재")
except TimeoutException :
    # 중복 계정 에러 없을 경우 여기로 넘어가
    try :
        # 회원가입 돼서 username 보일때까지 기다리고 있으면 성공으로 띄워줘
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid = 'text-welcome-username']")))
        print(f"회원가입 성공! 유저 이름 : {username.text}")  
    except TimeoutError :
        # 아예 둘다 안뜸 (페이지 로딩 문제 등)
        print("회원가입 실패")
        
cookies = driver.get_cookies()

if not cookies :
    print("쿠키가 비어 있습니다")
    
else :
    cookies_path = os.path.join("tests/exam", "cookies.json")
    with open(cookies_path, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii = False, indent = 2)
        print("쿠키가 JSON 파일로 저장되었습니다.")
    
