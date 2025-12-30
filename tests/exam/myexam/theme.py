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
chrome_options.add_argument("--no-sandbox") # 보안 기능 비활성화
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

# 테마 버튼 누르기
driver.find_element(By.XPATH, "//button[contains(@data-testid, 'theme')]").click()

# UI 바뀐거 테스트
try :
    theme_change = wait.until(
        EC.presence_of_element_located((By.XPATH, "//html[@class = 'dark']"))
    )
    print("테스트 성공 - 다크모드로 바뀌었습니다.")
    
except NoSuchElementException :
    print("테스트 실패 - 다크모드로 바뀌지 않았습니다.")