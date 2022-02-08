import urllib.request
from fake_useragent import UserAgent

#url = 'http://info.cern.ch'
# request = urllib.request.Request(url)  # request객체를 하나 만들어 줌
# response = urllib.request.urlopen( request) 

# print( response.read() )

# agent = UserAgent()
# header = {'User-Agent' : agent.chrome}

# url = 'https://image.zdnet.co.kr/2022/01/01/e601fd8d72cc33ca75cd9d41d3315684.jpg'
# request = urllib.request.Request( url, headers = header)
# response = urllib.request.urlopen( request )
# print(response.read())


# # urllib은 urlretrieve 함수를 이용해서 한 번에 파일로 저장할 수 있음
# url = 'https://image.zdnet.co.kr/2022/01/01/e601fd8d72cc33ca75cd9d41d3315684.jpg'
# # 파일을 저장할 경로
# path = 'web/data/download.jpg'
# # opener 객체를 생성해서 헤더를 수정해준다.
# opener = urllib.request.build_opener()

# agent = UserAgent()
# header = {'User-Agent' : agent.chrome}

# opener.addheaders = [('User-Agent', agent.chrome)]
# urllib.request.install_opener(opener)
# urllib.request.urlretrieve( url, path )

# 접근권한만 있다면 3줄로도 가능
url = 'https://images.unsplash.com/photo-1641063157251-ae9d815e5daa?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=710&q=80'
path = 'web/data/download2.jpg'
urllib.request.urlretrieve( url, path )

url = 'https://imgnews.pstatic.net/image/009/2022/01/03/0004903208_002_20220103105202076.jpg?type=w647'
path = 'web/data/download3.jpg'
urllib.request.urlretrieve( url, path )

