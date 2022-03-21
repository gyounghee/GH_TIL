from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

from . import views
# Django auth에 내장되어 있는 LoginView, LogoutView를 사용하기 위함 (앱 폴더의 views.py에 따로 코드를 작성할 필요 없음)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # template_name은 url 설정을 편하게 하기 위해 별칭을 준 것
    path('signIn/', auth_views.LoginView.as_view(template_name='accounts/signin.html') ),
    path('signOut/', auth_views.LogoutView.as_view() ),
    path('signUp/', views.signup),
    path('createUser/', views.createUser),
]