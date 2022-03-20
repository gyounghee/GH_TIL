# 네이버 영화 리뷰 페이지 크롤링
import requests 
import bs4    # BeautifulSoup 패키지 임포트

url = 'https://movie.naver.com/movie/point/af/list.naver'
response = requests.get(url)
html = response.text   # 이건 일반 텍스트이기 때문에 
review = bs4.BeautifulSoup(html)  # html을 BeautifulSoup 객체로 변환해줌
# type(review)   #  bs4객체인 것을 알 수 있음  →  문자열이 아님
#print(review)

# # 리뷰만 확인
# search = {
#     'class' : 'title'
# }
# td_elements = review.find_all('td', attrs = search)

# print(td_elements[0].text.split('\n')[5]) # 텍스트만 다 뽑아와서 나누고 리뷰가 들어있는 위치의 요소 출력

# for element in td_elements:
#     print( element.text.split('\n')[5])

# for element in td_elements:
#     title = element.find('a').text
#     score = element.find('em').text
#     review = element.text.split('\n')[5]
#     print(f'영화제목: {title}')
#     print(f'영화평점: {score}')
#     print(f'영화리뷰: {review}')
#     print()

# 1~10페이지까지 내용 스크래핑
search = {
    'class' : 'title'
    }

for p in range(1,2) :
    url = f'https://movie.naver.com/movie/point/af/list.naver?&page={p}'
    response = requests.get(url)
    html = response.text   # 이건 일반 텍스트이기 때문에 
    review = bs4.BeautifulSoup(html)

    #td_elements = review.find_all('td', attrs = search)
    td_elements = review.select('td.title')

    print('-------------------------------------------------------')
    print('페이지 번호 : ',p)

    for element in td_elements:
        title = element.find('a').text
        score = element.find('em').text
        review = element.text.split('\n')[5]
        print(f'영화제목: {title}')
        print(f'영화평점: {score}')
        print(f'영화리뷰: {review}')
        print()

