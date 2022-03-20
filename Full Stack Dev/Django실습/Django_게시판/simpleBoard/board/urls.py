from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.list , name='list'),  # view랑 연결  
    path('login/', views.login ),  
    path('write/', views.write ),  
    path('create', views.create),

    # 강사님이랑 같이 실습 - 삭제, 수정, 열람
    path('delete/',views.delete),
    path('update/',views.update),
    path('modify/',views.modify),
    # request http://~~/view/   → django → viwe
    path('view/', views.view),
    path('login/',views.login),


    # ## 혼자 실습 - 삭제, 수정, 열람
    # # Board를 삭제하기 위해 추가
    # path('deleteboard/',views.deleteboard),

    # # Board를 수정 & 수정 내용 list에 반영
    # path('amendboard/',views.amendboard),
    # path('amend',views.re_create),

    # # Board 내용 확인 & 확인 후 다시 list로 돌아가기
    # path('confirmboard/',views.confirmboard),
    # path('confirm',views.back),
]
