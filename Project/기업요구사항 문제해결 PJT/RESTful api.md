### 개념
    * REST (Representational State Transfer)   
        - 클라이언트 ↔ 서버의 통신방식   
        - URI와 HTTP를 이용한, 통신 목적의 아키텍처 스타일(유형)   
            +) URI(Uniform Resource Identifier)    
                : 문서, 그림, 영상 등의 자원 식별용 이름(경로)    
            +) 아키텍처 스타일 : 아키텍처(구조)의 종류(유형, 스타일, 타입)
                ex) 클라이언트/서버,  저장소,  파이프/필터,   REST
        - REST는 아키텍처 제작 시 사용되는 가이드 정도의 의미로 사용되며 명확히 준수해야할 표준은 없다

    * RESTful
        - REST가 적용된 시스템

    * REST API
        - REST가 적용된 API

    * RESTful
        - REST API를 제공하는 시스템


### REST의 6가지 조건
    * REST는 6가지 조건을 만족해야 함
        1. 일관된 인터페이스
            - URI 사용, HTTP 메소드 사용, RPC 미호출 등의 `지정된 인터페이스`를 준수
        2. 클라이언트/서버 (Client-Server)
            - 클라이언트는 서버에 `요청(request) 메세지`를 전송하고
            - 서버는 요청에 대한 `응답(response) 메세지`를 전송한다
        3. 비연결성(Statelessness)
            - 세션 등 `이전 상황(문맥)` 없이도 통신할 수 있다
        4. 캐시 가능 (Cacheable)
            - 서버의 응답 메세지는 `캐싱(저장 후 재사용)`될 수 있다.
        5. 계층화된 시스템 (Layered system)
            - 계층별로 기능이 분리된다.
            - 그러므로 중간 계층의 기능(로드 밸런싱, 서버증설, 인증 스스템 도입 등)이 변경되어도 통신에 영향을 주지 않는다.
        6. 주문형 코드(code on demand) (선택)
            - 손쉬운 데이터 처리를 위해 서버는 클라이언트에서 실행될 스크립트를 전송할 수 있다.


### REST API 만들기
    * API는 기본적인 CRUD를 위해 사용됨
    * API가 필요한 URL을 만들 때 
        - 표준을 만드는 것이 중요!!! (명확한 패턴)
        - URL에서는 동사를 사용하지 않는다. (명사만 사용)
        - 동사를 쓰는 대신에 HTTP methods를 사용하여 인터랙션 
            - HTTP methods : GET(읽기), POST(생성), PUT(업데이트), DELETE(삭제)
        - **`HTTP methods + 명사`** 방식을 사용 

### REST, REST API, RESTful의 개념, 설계 기본 규칙, 예시 등 
            - 참고자료 
                - https://gmlwjd9405.github.io/2018/09/21/rest-and-restful.html 
                - https://sanghaklee.tistory.com/57


### * restful api server 만들기 

+) api server를 테스트 하기 위한 툴 설치 
    - 테스트 툴은 `insomnia` 활용 

1. conda activate 가상환경
    - 가상환경 : p_youtube

2. pip install --upgrade pip 

3. pip install django

4. django-admin startproject 프로젝트이름
    - 프로젝트 이름 : restfulapiserver

5. Django REST framework 사용을 위한 설치   
    : 간단한 설정만으로 django를 restful api server로 만들어주는 프레임워크
    - pip install djangorestframework
    - pip install markdown
    - pip install django-filter

6. settings.py에 source 추가  
    - 공식 홈페이지 참고 ( https://www.django-rest-framework.org/ )
    1. ALLOEWED_HOST에 (*) 추가
        ```python
        ALLOWED_HOSTS = ['*']
        ```
    2. INSTALLED_APPS에 'rest_framework' 추가    
        ```python
        INSTALLED_APPS += [
            'rest_framework'
        ]
        ```
    3. REST_FRAMEWORK 추가  
        ```python
        REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
            ]
        }
        ```
    - Django는 앱 단위로 관리하기 때문에 방금 설치한 rest_framework 앱을 명시해 주어야 하며, rest_framework에 권한 설정을 하기 위한 설정도 넣어줌

7. 프로젝트폴더 > urls.py 에 코드 추가    
    -   
    ```python
    from django.urls import path, include

    urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls')),
    ]
    ```

8. superuser 생성
    - python manage.py createsuperuser
        - 생성한 id, pw, email
        - id : superuser /  pw : 0000  / email : superuser@naver.com 

9. python manage.py startapp 앱이름 
    - 앱 이름 : addresses

10. 앱폴더 > models.py에 모델 생성
    -   
    ```python
    class Addresses(models.Model):
    name = models.CharField(max_length=10)
    address = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 조회 시 created를 기준으로 내림차순으로 표시됨 (순서대로 표시하기 위함)
        ordering = ['created']
    ```

11. migration하기 
    - python manage.py makemigrations 앱이름
    - python manage.py migrate

12. 앱폴더 > serializers.py 파일 생성 후 코드 추가   
    - 
    ```python
    from rest_framework import serializers
    from .models import Addresses    

    class AddressesSerializer(serializers.ModelSerializer):
        class Meta:
            model = Addresses
            fields = ['name','address','created']
    ```

13. 앱 폴더 > views.py   
    -   
    ```python
    from django.shortcuts import render
    from django.http import HttpResponse, JsonResponse
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.parsers import JSONParser

    from .models import Addresses
    from .serializers import AddressesSerializer

    ## 모든 건수 조회하는 코드
    @csrf_exempt
    def address_list( request ) :
        # GET요청이 들어오면 전체 address list를 내려주는  
        if request.method == 'GET':
            query_set = Addresses.objects.all()
            serializer = AddressesSerializer(query_set, many=True)  
            return JsonResponse(serializer.data, safe=False)
        
        # POST 요청이 들어오면 만들어주도록 
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = AddressesSerializer(data=data)
            if serializer.is_valid() :    
                serializer.save()   
                return JsonResponse(serializer.data, status=201)  
            return JsonResponse(serializer.errors, status=400)  
    ```

14. 프로젝트폴더 > urls.py 에 코드 추가 
    -      
    ```python
    from django.contrib import admin
    from django.urls import path, include
    from addresses import views  

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api-auth/', include('rest_framework.urls')),
        path('addresses/', views.address_list),
]
    ```

15. (선택) 시간 설정을 한국시간으로 설정
    - 프로젝트 폴터 > settings.py
    ```python
    # 변경해줘야할 코드
    TIME_ZONE = 'Asia/Seoul'
    USE_TZ = False
    ```


# **TEST** - `insomnia`
    - `Ctrl+N`을 하여 request생성
        1. GET http://127.0.0.1:8000/addresses/
            - 저장된 데이터들이 JSON형태로 보이면 성공
        
        2. POST http://127.0.0.1:8000/addresses/
            - JSON 형태로 데이터를 보내줘야함 
            ```python
            {
                "name" : "경이",
                "address" : "집"
            }
            ```

            - 결과가 이렇게 나온다면 성공 
            ```python
                {
                    "name": "경이",
                    "address": "집",
                    "created": "2022-03-22T10:08:45.107967Z"
                }
            ```

**위에서 했던 것이 다수의 건수를 조회하는 코드였다면 이번에는 단건 조회에 대해 살펴보자.**

16. 앱 폴더 > views.py
    - 단건 조회 코드 추가  
    ```python
    @csrf_exempt
    def address( request, pk ) :   # 단건 조회
        select_adr = Addresses.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = AddressesSerializer(select_adr)  
            return JsonResponse(serializer.data, safe=False)
        
        elif request.method == 'PUT' :
            data = JSONParser().parse(request)
            serializer = AddressesSerializer(select_adr, data=data)
            if serializer.is_valid() :    
                serializer.save()  
                return JsonResponse(serializer.data, status=201) 
            return JsonResponse(serializer.errors, status=400)

        elif request.method == 'DELETE' :
            select_adr.delete()  
            return HttpResponse(status=204) 
    ```

17. 프로젝트 폴더 > urls.py
    - urlpatterns = [] 에 코드 추가
    ```python
    path('addresses/<int:pk>', views.address),
    ```


**이번엔 DB에 저장된 PW가 사용자가 입력한 PW가 맞는지 확인 후 응답보내기**

18. 앱 폴더 > views.py
    - 코드 추가
    ```python
    @csrf_exempt
    def login(request) :
        if request.method == 'POST':
            data = JSONParser().parse(request)
            search_name = data['name']
            select_adr = Addresses.objects.get(name=search_name)
            # print(data['address'])     #  읽어온 비밀번호
            # print(select_adr.address)  #  저장된 비밀번호 
            if data['address'] == select_adr.address :
                return HttpResponse(status=200)
            else :
                return HttpResponse(status=400)
    ```

19. 프로젝트 폴더 > urls.py
    - urlpatterns =[] 에 코드 추가
    ```python
    path('login/', views.login),
    ```