import requests  # requests는 설치가 필요한 패키지(pip install requests)
from fake_useragent import UserAgent

# url = 'http://info.cern.ch'
# response = requests.get(url)
# print(response.text)

agent = UserAgent()
header = {'User-Agent' : agent.chrome}

url = 'https://image.zdnet.co.kr/2022/01/01/e601fd8d72cc33ca75cd9d41d3315684.jpg'
response = requests.get(url, headers = header)
#print(response.content )

# 파일을 저장하려면 오픈해서 저장해야한다.
with open('web/data/download4.jpg','wb') as file :   # 'wb' →  binary 형태로 열어서 저장해야함  
    file.write( response.content )