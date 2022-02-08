from django.urls import path, include

# view와 연결
from . import views   # views에 있는 모든 내용 import


urlpatterns = [
    # 해당 URL 패턴을 views.py의 index 함수와 연결
    # 입력을 처리하고 다시 첫 페이지로 돌아가기 위해서 name 추가 
    path('',views.index, name='index'),

    # createTodo에 대한 URL 요청과 view를 연결해준다.
    path('createTodo/', views.createTodo),

    # deleteTodo에 대한 URL 요청과 view를 연결해준다.
    path('deleteTodo/', views.deleteTodo),
]
