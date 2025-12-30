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

try :
    # login and check session
    driver.find_element(By.XPATH, "//button[@data-testid = 'link-login']").click()
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("1234")
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-login-submit']").click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid = 'text-welcome-username']")))
    print("STEP 1 - 로그인 성공")
    
    # Get cookie
    cookies = driver.get_cookies()
    login_cookie = os.path.join("tests/exam", "login_cookies.json")
    
    with open(login_cookie, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=4)
        print("STEP 2 - 쿠키 JSON 파일로 저장 완료")
    
    # Create Post for clicking 'create post' button and check session
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-create-post']").click()
    driver.find_element(By.XPATH, "//input[@data-testid = 'input-post-title']").send_keys("테스트입니다")
    driver.find_element(By.XPATH, "//textarea[@data-testid = 'textarea-post-content']").send_keys("테스트 내용입니다")
    driver.find_element(By.XPATH, "//input[@data-testid = 'input-post-category']").send_keys("테스트1 ,테스트2")
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-create-post']").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[text() = 'Post created successfully']")))
    
    # Get URL of the created post
    current_url = driver.current_url
    current_url_parts = current_url.split('/')
    post_id = current_url_parts[-1]
    
    # Back to Home and check post
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-back-home']").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@data-testid = 'card-post-{post_id}']")))
    title = driver.find_element(By.XPATH, f"//div[@data-testid = 'text-post-title-{post_id}']").text.strip()
    if title == "테스트입니다":
        print("STEP 3 - 게시글 생성 완료")
    else :
        print("STEP 3 - 게시글 생성 실패")

    # Update Post for clicking 'edit post' button and check session
    driver.find_element(By.XPATH, f"//div[@data-testid = 'card-post-{post_id}']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-edit-post']").click()
    time.sleep(2)
    
    title_input = driver.find_element(By.XPATH, "//input[@data-testid = 'input-post-title']")
    title_input.click()
    title_input.send_keys(Keys.CONTROL, 'a')
    title_input.send_keys(Keys.DELETE)
    title_input.send_keys("수정된 테스트입니다")
    
    content_input = driver.find_element(By.XPATH, "//textarea[@data-testid = 'textarea-post-content']")
    content_input.click()
    content_input.send_keys(Keys.CONTROL, 'a')
    content_input.send_keys(Keys.DELETE)
    content_input.send_keys("수정된 테스트 내용입니다")
    
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-update-post']").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[text() = 'Post updated successfully']")))
    
    # Back to Home and check updated post
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-back-home']").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@data-testid = 'card-post-{post_id}']")))
    updated_title = driver.find_element(By.XPATH, f"//div[@data-testid = 'text-post-title-{post_id}']").text.strip()
    if updated_title == "수정된 테스트입니다":
        print("STEP 4 - 게시글 수정 완료")
    else:
        print("STEP 4 - 게시글 수정 실패")
        
    # Delete Post for clicking 'delete post' button and check session
    driver.find_element(By.XPATH, f"//div[@data-testid = 'card-post-{post_id}']").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "//button[@data-testid = 'button-delete-post']").click()
    
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[text() = 'Post deleted successfully']")))
    
    # Back to Home and check deleted post
    titles = driver.find_elements(By.XPATH, f"//div[@data-testid = 'text-post-title-{post_id}']")
    if len(titles) == 0 :
        print("STEP 5 - 게시글 삭제 완료")
    else :
        print("STEP 5 - 게시글 삭제 실패")
    
except NoSuchElementException :
    print("요소를 찾을 수 없습니다. 테스트 실패.")
