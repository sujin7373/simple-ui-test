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

def success_signup_test() :
    try :
        # 회원가입 페이지로 이동
        driver.get("http://localhost:5000/signup")
        time.sleep(3)

        # 요소 찾고 입력
        driver.find_element(By.ID, "username").send_keys("hjhj")
        driver.find_element(By.ID, "password").send_keys("zxcv")
        driver.find_element(By.ID, "confirmPassword").send_keys("zxcv")

        # 회원가입 하기 버튼 클릭
        driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
    
        # 회원가입 돼서 username 보일때까지 기다리고 있으면 성공으로 띄워줘
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid = 'text-welcome-username']")))
        print(f"테스트 성공 - 유저 이름 : {username.text}")  
        
    except NoSuchElementException :
        # 페이지 로딩 문제 등으로 요소 못찾음
        print("테스트 실패")
        
    finally :
        # 예외 발생 여부와 관계 없이 무조건 실행되는 코드
        driver.quit()
        

def duplicate_fail_signup_test() :
    try :
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", False)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        
        # 회원가입 페이지로 이동
        driver.get("http://localhost:5000/signup")
        time.sleep(3)

        # 요소 찾고 입력
        driver.find_element(By.ID, "username").send_keys("io89")
        driver.find_element(By.ID, "password").send_keys("qw12")
        driver.find_element(By.ID, "confirmPassword").send_keys("qw12")
        driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        
        # 회원가입 후 로그아웃
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid = 'text-welcome-username']")))
        driver.find_element(By.XPATH, "//button[@data-testid = 'button-user-menu']").click()
        driver.find_element(By.XPATH, "//div[@data-testid = 'button-logout']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@data-testid = 'link-signup']").click()
        time.sleep(3)
        
        # 위와 똑같은 유저 이름으로 로그인 
        driver.find_element(By.ID, "username").send_keys("io89")
        driver.find_element(By.ID, "password").send_keys("qw12")
        driver.find_element(By.ID, "confirmPassword").send_keys("qw12")
        driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        
        # 해당 에러 메세지 나타날 때 까지
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'already')]")))
        print("테스트 성공 - 중복 계정 존재")
        
    except NoSuchElementException :
        # 페이지 로딩 문제 등으로 요소 못찾음
        print("테스트 실패")
        
    finally :
        # 예외 발생 여부와 관계 없이 무조건 실행되는 코드
        driver.quit()
   
     
def password_confirm_fail_test() :
    try :
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", False)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        
        # 회원가입 페이지로 이동
        driver.get("http://localhost:5000/signup")
        time.sleep(3)

        # 요소 찾고 입력
        driver.find_element(By.ID, "username").send_keys("ad111")
        driver.find_element(By.ID, "password").send_keys("qwer1234")
        driver.find_element(By.ID, "confirmPassword").send_keys("qwer")

        # 회원가입 하기 버튼 클릭
        driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        
        # confirm password 틀려서 'Passwords do not match' 오류 메세지 보일 때 까지
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'match')]")))
        print("테스트 성공 - confirm password 틀림")
        
    except NoSuchElementException :
        print("테스트 실패")
        
    finally :
        driver.quit()
        

def less_username_test() :
    try :
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("detach", False)
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 10)
        
        driver.get("http://localhost:5000/signup")
        time.sleep(3)
        
        # 3글자 보다 적게 username 치고 버튼 누를 경우
        username = driver.find_element(By.CSS_SELECTOR, '#username')
        username.send_keys('ad')
        driver.find_element(By.ID, "password").send_keys("password")
        driver.find_element(By.ID, "confirmPassword").send_keys("password")
        
        # driver.find_element(By.XPATH, '//button[@type = "submit"]').click()
        # reportValidity() - 메시지를 보이게 만드는 트리거
        # 해당 폼 요소에 대해 유효성 검사를 수행하고 툴팁을 표시하도록 함
        # 그래서 저 click()을 안해도 됌
        driver.execute_script("arguments[0].reportValidity();", username)
        time.sleep(3)
        
        # username의 유효성 상태에 따라 브라우저가 사용자에게 보여줄 문자열 메시지 반환
        msg = driver.execute_script("return arguments[0].validationMessage;", 
    username)
        
        assert msg != "", "테스트 실패 - 브라우저 유효성 메시지가 비어있습니다."
        assert "3자 이상" in msg, "테스트 실패 - 브라우저 유효성 메시지가 올바르지 않습니다."
        
        print(f"테스트 성공 - msg : {msg}")
        
    except NoSuchElementException :
        print("테스트 실패 - 예기치 못한 오류")
        
    finally :
        driver.quit()
        

# def less_password_test()
# def zero_username_test()
# def zero_password_test()
# def zero_confirm_password_test()

# 이 파일을 직접 실행할 시 이 코드들이 실행된다    
if __name__ == "__main__":
    print("\n=== 회원가입 테스트 ===\n")
    
    print("Test 1: 회원가입 정상 테스트")
    success_signup_test()
    
    print("\nTest 2: 중복된 유저네임 테스트")
    duplicate_fail_signup_test()
    
    print("\nTest 3: 패스워드 불일치 테스트")
    password_confirm_fail_test()
    
    print("\nTest 4: 3자 미만 유저네임 기입 테스트")
    less_username_test()
    
    print("\n=== 모든 회원가입 테스트 완료 ===\n")