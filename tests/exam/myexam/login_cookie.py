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
chrome_options.add_experimental_option("detach", False)

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10) # 요소가 바로 안 나타나도 최대 10초까지 재시도하며 기다려

# WebDriverWait 쓰기 위한 초기 작업
wait = WebDriverWait(driver, 10)

driver.get("http://localhost:5000")
time.sleep(3)
print("페이지 이동 완료")

# 로그인 버튼 찾아서 클릭&로그인 페이지로 이동
driver.find_element(By.XPATH, "//button[@data-testid = 'link-login']").click()

try :
    # 요소 뜰때까지 기다리기
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//button[@data-testid = 'button-login-submit']"))
    )
    
    # 입력하고 Sign In 버튼 누르기
    driver.find_element(By.ID, "username").send_keys("doremi73")
    driver.find_element(By.ID, "password").send_keys("soojin0703")
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-login-submit']").click()
    
    try :
        # 유저 이름 뜰 때까지 기다리기
        user_name = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@data-testid, 'welcome')]"))
        )
        print(f"로그인 성공! 유저 이름 : {user_name.text}")
        
    except NoSuchElementException :
        # 유저 이름이 안 뜸 (페이지 미로딩 등으로)
        print("회원가입 실패")
    
except NoSuchElementException :
    # 로그인 페이지로 안 넘어가짐
    print("로그인 페이지가 로딩되지 않았습니다")
    
save_cookie = driver.get_cookies()

if not save_cookie :
    print("쿠키가 비어 있습니다.")
    
else :
    login_cookies_path = os.path.join("tests/exam", "login_cookies.json")
    
    with open(login_cookies_path, "w", encoding="utf-8") as f:
        json.dump(save_cookie, f, ensure_ascii=False, indent=2)
        print("로그인 정보 쿠키가 JSON 파일로 저장되었습니다.")
