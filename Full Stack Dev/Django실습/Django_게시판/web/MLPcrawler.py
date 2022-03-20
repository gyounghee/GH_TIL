from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time

service = Service(executable_path = "C:\\Users\\user\\workspace\\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(service=service, options=options)

url = 'https://lc.multicampus.com/k-digital/#/login'
browser.get( url )

# page가 로딩되는 시간이 있는데 로딩되기 전에 요소를 찾으려고 하면 없다고 나옴
# 페이지가 로딩되고 나서 요소를 찾기 위해 time을 줌
time.sleep(2)
inputs = browser.find_elements(By.CSS_SELECTOR, 'div.input-row-line input')
loginButton = browser.find_element(By.CSS_SELECTOR, 'div.btn-row button.login-btn')

inputs[0].send_keys('ghl0209')
inputs[1].send_keys('rudgml97!')
# inputs[1].send_keys('rudgml97!\n')   이렇게하면 바로 버튼을 누르지않고 enter로 바로 로그인
loginButton.click()

# 무한 스크롤 구현 ( 모든 내용을 전부 스크래핑)
# 초기 높이를 가져옴
last_height = browser.execute_script('return document.body.scrollHeight')
while True:
    # 스크롤을 아래로 내렴
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight);') # 자바크스립트 이용해서 처음부터 끝까지 스크롤 해주는 코드
    time.sleep(2)  # 페이지 내용이 로딩되는 동안 잠시 기다려줌
    
     # 새로 높이를 잼
    new_height = browser.execute_script('return document.body.scrollHeight')
    
    # 높이가 전과 같을경우 더이상 내려갈 곳이 없다고 판단 되면 종료
    if new_height == last_height : break
    # 그렇지 않으면 새로운 높이로 변경하고 다음 회차로 ~
    last_height = new_height

# 로드된 내용들을 수집
articles =  browser.find_elements (By.CSS_SELECTOR, 'div.feedlist span article') # article 전체를 가져옴
# title = browser.find_elements (By.CSS_SELECTOR, 'div.feed-tit')
# content = browser.find_elements (By.CSS_SELECTOR, 'div.fee-cont')

for article in articles :
    for content in article.find_elements(By.CSS_SELECTOR, 'span.feedContentBlk'):
        print(content.text)