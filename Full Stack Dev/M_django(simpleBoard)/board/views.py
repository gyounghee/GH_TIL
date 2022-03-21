from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse

from .models import Board

# Create your views here.
def index( request ):
    rows = Board.objects.all()
    content = {'rows': rows}
    return render(request, 'board/list.html', content)

def login( request ):
    return render( request, 'board/login.html')

def write( request ):
    return render(request, 'board/write.html')


# decorator를 이용해서 로그인이 필요한 함수를 지정
from django.contrib.auth.decorators import login_required
@login_required(login_url='/accounts/signIn/')
def create( request ):
    if request.method == 'POST':
        new = Board( 
            user        = request.user,
            createDate  = request.POST['createDate'], 
            subject     = request.POST['subject'],
            content     = request.POST['content'],
        )
        new.save()
        return HttpResponseRedirect( reverse('list') )
    else : # 로그인이 되어 있지 않은 경우 로그인 이후에 새로 글을 작성
        return render( request, 'board/write.html')

@login_required(login_url = '/accounts/signIn/')
def delete( request ):
    b = Board.objects.get(id = request.POST['id'] )
    b.delete()
    return HttpResponseRedirect( reverse('list') )

@login_required(login_url = '/accounts/signIn/')
def update( request ):
    contents = Board.objects.get(id = request.GET['id'])
    content = {'contents': contents}
    return render(request, 'board/update.html', content)

@login_required(login_url = '/accounts/signIn/')
def modify( request ):
    update_b = Board.objects.get(id = request.POST['id'])
    update_b.createDate = request.POST['createDate']
    update_b.user = request.POST['user']
    update_b.subject = request.POST['subject']
    update_b.content = request.POST['content']
    update_b.save()
    return HttpResponseRedirect( reverse('list') )

def view( request ):
    contents = Board.objects.get(id=request.GET['id'])
    content = {'contents':contents} 
    return render( request, 'board/view.html', content )
