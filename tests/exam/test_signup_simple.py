"""
회원가입 테스트 - 가장 간단한 버전
학생들이 이해하기 쉽도록 최대한 간단하게 작성함
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 생성
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

try:
    # 1단계: 회원가입 페이지로 이동
    print("회원가입 페이지로 이동 중...")
    driver.get("http://localhost:5000/signup")
    time.sleep(2)
    print("✓ 페이지 로드 완료")
    
    # 2단계: 사용자명 입력
    print("\n사용자명 입력 중...")
    username_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-username"]')
    username_input.clear()
    username_input.send_keys("testuser123")
    print("✓ 사용자명: testuser123")
    
    # 3단계: 비밀번호 입력
    print("비밀번호 입력 중...")
    password_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-password"]')
    password_input.clear()
    password_input.send_keys("password123")
    print("✓ 비밀번호 입력 완료")
    
    # 4단계: 비밀번호 확인 입력
    print("비밀번호 확인 입력 중...")
    confirm_password_input = driver.find_element(By.CSS_SELECTOR, '[data-testid="input-confirm-password"]')
    confirm_password_input.clear()
    confirm_password_input.send_keys("password123")
    print("✓ 비밀번호 확인 입력 완료")
    
    # 5단계: 회원가입 버튼 클릭
    print("\n회원가입 버튼 클릭 중...")
    signup_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="button-signup-submit"]')
    signup_button.click()
    print("✓ 버튼 클릭 완료")
    
    # 6단계: 페이지 이동 대기
    print("페이지 이동 중... (3초 대기)")
    time.sleep(3)
    
    # 7단계: 현재 URL 확인
    current_url = driver.current_url
    print(f"\n현재 URL: {current_url}")
    
    if "/" in current_url:  # 홈페이지로 이동했는지 확인
        print("✓ 홈페이지로 이동 성공!")
    
    # 8단계: 사용자 정보 표시되는지 확인
    print("\n사용자 정보 확인 중...")
    try:
        username_text = driver.find_element(By.CSS_SELECTOR, '[data-testid="text-username"]')
        print(f"✓ 사용자명 표시됨: {username_text.text}")
    except:
        print("! 사용자명이 표시되지 않음")
    
    print("\n✓✓✓ 회원가입 테스트 완료!")

except Exception as e:
    print(f"\n✗ 오류 발생: {str(e)}")

finally:
    # 브라우저 종료
    print("\n브라우저를 닫고 있습니다...")
    driver.quit()
    print("✓ 완료")
