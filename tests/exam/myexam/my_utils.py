def generate_unique_username():
    """Generate a unique username for testing."""
    timestamp = int(time.time() * 1000)
    return f"testuser_{timestamp}"


def get_driver():
    """Create and return a Chrome WebDriver instance."""
    chrome_options = Options()
    # Set HEADLESS=true for headless mode (default is false for local browser window)
    if os.environ.get("HEADLESS", "false").lower() != "false":
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver

# 무한 스크롤 함수
def infinite_scroll(driver) :
    # 현재 페이지의 전체 높이(맨 아래 위치)를 가져와 저장
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    
    while True :
        # 페이지 맨 아래로 스크롤
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        # 스크롤 이후의 전체 페이지 높이를 다시 측정
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        # 페이지 높이가 그대로라면
        if new_height == last_height :
            time.sleep(1)
            # 한번 더 비교 -> 그래도 변화 없으면 while 종료
            if new_height == driver.execute_script("return document.documentElement.scrollHeight") :
                break
        else :
            # 새 콘텐츠가 로딩됐으면 last_height 갱신하고 스크롤 다시 반복
            last_height = new_height