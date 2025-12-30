from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import os
import json
import time

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")
# 스크립트 끝나고 브라우저 열리게 하기 - True
# 스크립트 끝나고 브라우저 닫히게 하기 - False
chrome_options.add_experimental_option("detach", False)

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

wait = WebDriverWait(driver, 10)
driver.get("http://localhost:5000/")
time.sleep(3)


def scroll_and_crawl(driver) :
    # 현재 문서의 전체 높이 저장
    scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
    step = 600 # 한 번에 스크롤할 픽셀 수
    position = 0 # 현재 스크롤 위치
    
    seen = set() # 중복 체크용 집합 만들기
    collected_posts = [] # 크롤링한 게시물 저장용 리스트 만들기
    
    # 현재 위치가 전체 높이보다 작을 동안 계속 반복
    while position < scroll_height :
        # 스크롤 하자
        driver.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(2)
        
        posts = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'card-post')]")

        for post in posts :
            title = post.find_element(By.XPATH, ".//div[contains(@data-testid, 'text-post-title')]").text.strip()
            author = post.find_element(By.XPATH, ".//span[contains(@data-testid, 'text-post-author')]").text.strip()
            date = post.find_element(By.XPATH, ".//span[contains(@data-testid, 'text-post-date')]").text.strip()
            if title not in seen :
                seen.add(title)
                collected_posts.append({
                    "제목" : title,
                    "저자" : author,
                    "날짜" : date
                })
                print(f"크롤링한 게시물 -> 제목 : {title} / 저자 : {author} / 날짜 : {date}")
               
        # 다음 스크롤 위치로 이동 
        position += step
        # 페이지 높이를 다시 계산
        scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
        
    return collected_posts


def save_posts_to_json(collected_posts) :
    all_posts_path = os.path.join("tests/exam", "all_posts.json")
    
    with open(all_posts_path, "w", encoding="utf-8") as f:
        json.dump(collected_posts, f, ensure_ascii=False, indent=4)
        print("모든 게시물을 JSON 파일로 저장했습니다.")
        

if __name__ == "__main__" :
    
    print("스크롤 및 크롤링 시작")
    collected_posts = scroll_and_crawl(driver)
    
    print("JSON 파일로 저장 시작")
    save_posts_to_json(collected_posts)
                