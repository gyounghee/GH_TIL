from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# 직접 User 모델 import  → 비추 
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model   → 이거는 추천한다고 함 블로그에서 
# make_password() 을 이용하면 hashed password를 생성할 수 있음
from django.contrib.auth.hashers import make_password

# Create your views here.

def signup( request ):
    return render(request, 'accounts/signup.html')

def createUser( request ):
    id = request.POST['id']
    pw = request.POST['pw']
    
    user = User(username=id, password=make_password(pw))
    user.save()

    return HttpResponseRedirect( reverse('list') )
