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

# 랜딩 페이지로 이동
driver.get("http://localhost:5000")
time.sleep(3)
print("페이지 이동 완료")

# 동일한 속성의 여러 요소들 가져오기
titles = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'text-post-title')]")
authors = driver.find_elements(By.XPATH, "//span[contains(@data-testid, 'text-post-author')]")
dates = driver.find_elements(By.XPATH, "//span[contains(@data-testid, 'text-post-date')]")

# posts에 데이터 저장
posts =[]

# zip으로 한큐에 for문 돌리기
for title, author, date in zip(titles, authors, dates) :
    post_data = {
        "제목" : title.text.strip(),
        "저자" : author.text.strip(),
        "날짜" : date.text.strip()
    }
    posts.append(post_data)

# path 지정 후 json 파일 쓰고 저장
recent_posts_path = os.path.join("tests/exam", "recent_posts.json")
with open(recent_posts_path, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent = 4)
    print("JSON 파일로 크롤링한 데이터를 저장했습니다.")
    