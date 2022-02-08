"""ToDoList URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 1. route가 빈 문자열이라는 것  →  기본경로로 사용한다는 의미
    # include를 이용해서 하위 'URLconf'를 호출
    path('', include('my_to_do_app.urls')),

    # 2. 앱별로 URL과 연결해주고 싶다면
    # path('my_to_do_app', include('my_to_do_appp.urls'))
    path('admin/', admin.site.urls),
]
