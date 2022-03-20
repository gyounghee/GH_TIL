import socket

# 네트워크 통신을 하기 위한 소켓 객체를 생성
# IPv4를 이용한 TCP통신용 소켓(파일 입/출력을 하기 위해서 객체를 생성하는 것과 비슷)
# 이렇게 생성한 소켓 객체를 통해서 서버와 통신(입/출력)을 할 수 있다
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("DEBUG:::소켓 생성 완료")

# 파일 입/출력 할 때 open을 통해서 입/출력 하기 위한 객체를 얻어온 것 처럼
# 통신(입/출력)하기 위한 서버와의 객체를 생성
# 소켓 프로그래밍에서는 connect()를 통해서 서버와 통신 하기 위한 서버의 객체를 얻어올 수 있다.
# 생성된 객체를 통해서 통신(입/출력)할 수 있다.

# 읽거나 쓰기 위한 파일의 경로와 유사
# 통신하기 위한 네트워크 상의 경로 정도로 이해
serverAddress = socket.gethostbyname('info.cern.ch')
serverPort = 80

# 오픈하기 위한 서버의 경로는 튜플로 전달
sock.connect( (serverAddress, serverPort) )
print('DEBUG:::connect 완료')

# 서버에 HTML 코드를 요청 => Request Header
# 대/소문자, 띄어쓰기 주의
request_header = 'GET /index.html HTTP/1.1\r\n'  # start-line(request-line) / GET :  클라이언트가 서버에게 URL에 해당하는 자료의 전송을 요청 
# +) request_header = 'HEAD /index.html HTTP/1.1\r\n'   # HEAD : HEAD : GET 요청으로 반환될 데이터 중 헤더 부분에 해당하는 데이터만(즉, 헤더만) 요청 → 많이 쓰는 메소드는 아님
# +) request_header = 'OPTIONS /index.html HTTP/1.1\r\n'  # OPTIONS : 해당 URL에서 지원하는 요청 메세지의 목록을 요청하는 메소드
request_header += 'Host: info.cern.ch\r\n'       # 헤더필드 : 헤더필드는 서버와 통신에 필요한 여러가지 정보를 표현
request_header += '\r\n'                         # 마지막에 들어가는 \r\n(CRLF)는 "헤더의 끝"을 의미

# 요청대로 처리가 되어서 HTML 코드가 잘 다운로드 되는지 확인 
sock.send( request_header.encode() )
response = sock.recv(1024)
print( response.decode() )

sock.close()

