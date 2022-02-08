from django.urls import path
from django.views.generic.base import TemplateView

from . import views
from board import views as board_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path( 'signIn/', auth_views.LoginView.as_view(template_name='check/signin.html') ),
    path( 'signOut/', auth_views.LogoutView.as_view() ),
    path( 'signUp/', views.signup),
    path( 'createUser/', views.createUser),
    path( 'check/', board_views.list),
]  