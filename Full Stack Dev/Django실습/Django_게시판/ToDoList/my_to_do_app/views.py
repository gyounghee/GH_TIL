from django.http.response import HttpResponseRedirect
from django.shortcuts import render

# HttpResponse를 통해 응답을 만들어주기 위해 추가
from django.http import HttpResponse
#  미리 만들어진 model을 가져오도록 한다
from .models import *
# index 페이지로 돌아가기 위한 reverse를 import
from django.urls import reverse

# Create your views here.
def index (request) :
    # DB의 내용을 브라우저에 전달하기 위한 코드
    todos = Todo.objects.all()   # DB 조회  (TABLE내의 모든 내용을 조회)
    content = {'todos':todos}    # 조회된 내용을 딕셔너리 형태로 content에 저장 
    return render( request, 'my_to_do_app/index.html', content)  # content내용을 브라우저에 전달 

def createTodo( request ) :
    # URL과 view가 잘 연결되었는지 확인하기 위해서 아래와 같은 코드를 이용
    # 페이지에서 메모하기 누르면 'create Todo를 할거야' 라는 응답이 씌여진 새 페이지 생성
    # return HttpResponse('create Todo를 할거야')

    # 사용자가 입력한 할 일을 잘 받아오는지 확인
    # 입력값 전달은 POST 방식으로, 'todoContent' 변수를 통해서 전달이 될거임
    #user_input_str = request.POST['todoContent']
    #return HttpResponse(f'사용자가 입력한 값 : {user_input_str}')
           
    user_input_str = request.POST[ 'todoContent' ]
    # models.py에서 정의된 클래스를 이용해서 전달받은 값을 DB에 저장한다.
    new_todo = Todo( content = user_input_str )
    new_todo.save()

    return HttpResponseRedirect(reverse('index'))

def deleteTodo( request ):
    # print('요청변수 :', request.GET['todoNum'])
    todo = Todo.objects.get(id = request.GET['todoNum'])
    todo.delete()
    return HttpResponseRedirect(reverse('index'))