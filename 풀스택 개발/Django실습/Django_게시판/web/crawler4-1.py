# 쇼핑몰 후기 가져오기 전 네이버 실습
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# 블루투스 오류 방지용
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# webdriver → webdriver를 이용하여 브라우저를 직접 제어가능
# chrom을 기준으로 현재 사용하고 있는 버전에 맞춰서 webdriver를 다운로드
service = Service(executable_path = "C:\\Users\\user\\workspace\\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=options)

url = 'https://www.naver.com'
browser.get( url )  # 브라우저 객체를 통해 확인

# 검색어 입력 후 엔터 입력
# element = browser.find_element(By.CSS_SELECTOR, 'input#query')
# element.send_keys('날씨')
# element.send_keys('\n') # enter를 날려서 검색완료까지 가능

#element = browser.find_element(By.CSS_SELECTOR, 'div.green_window')
#print( element.get_attribute('innerHTML') )

# 검색어 입력 후 마우스 클릭
# 클릭 가능한 요소라면 클릭이 가능
# input = browser.find_element(By.CSS_SELECTOR, 'input#query')
# button = browser.find_element(By.CSS_SELECTOR, 'button#search_btn')
# input.send_keys('검색어')
# button.click()

# input2 = browser.find_element(By.CSS_SELECTOR, 'input#query')
# input2.clear()
# input.send_keys('두 번째 검색어')
# button.click()

# 개인 실습 - 뉴스 보기
# news = browser.find_element(By.CSS_SELECTOR, 'a[href="https://news.naver.com/" ]')
# news.click()
