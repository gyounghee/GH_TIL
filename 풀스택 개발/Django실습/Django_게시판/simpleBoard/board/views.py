from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# 다시 list페이지로 돌아가기 위해 reverse를 import
from django.urls import reverse

from board.models import *

# Create your views here.

def list( request ) :
    # DB의 board 테이블의 모든 내용을 가져온다.
    rows = Board.objects.all()
    content = {'rows' : rows}

    return render(request, 'board/list.html', content)

def login( request ) :
    return render(request, 'board/login.html')

def write( request ) :
    #return HttpResponse('게시글 쓰기와 연결')
    return render(request, 'board/write.html')

#def create( request ):
#    return HttpResponse('게시글을 생성합니다.')

#데코레이터를 이용해서 로그인이 필요한 경우
from django.contrib.auth.decorators import login_required
@login_required(login_url='/check/signIn/')
def create( request ):

    if request.method == 'POST':
        new = Board(
            user       = request.user,
            createDate = request.POST['createDate'],
            subject    = request.POST['subject'],
            content    = request.POST['content'],
        )
        new.save()
        return HttpResponseRedirect( reverse('list') )
    else:
        # 로그인이 되어있지 않은 경우 로그인 이후에 새로 글을 작성해준다
        return render(request, 'board/write.html')


# 강사님이랑
# 삭제
@login_required(login_url='/check/signIn/')
def delete(request):
    
    b = Board.objects.get(id=request.POST['id'])
    print('삭제을 요청한 사용자의 id : ', request.user)
    print(' 게시판의 소유자 id: ',b.user)

    if request.user != b.user :
        return render( request, 'board/alert.html')
    else :
        b.delete()
        return HttpResponseRedirect( reverse('list') )

# 수정하기 위해 수정 창 띄움
@login_required(login_url='/check/signIn/')
def update( request ) :
    post = Board.objects.get(id=request.GET['id'])
    content = {'post' : post}
    return render(request, 'board/update.html', content)

# 수정한 후 다시 board로 돌아감
from django.contrib import messages
@login_required(login_url='/check/signIn/')
def modify(request) :    

    post = Board.objects.get(id=request.POST['id'])
    print('수정을 요청한 사용자의 id : ', request.user)
    print(' 게시판의 소유자 id: ',post.user)
    
    if request.user != post.user :
        return render( request, 'board/alert.html')
    else :
        post.createDate = request.POST['createDate']
        post.subject = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return HttpResponseRedirect(reverse('list'))

def view( request ):
    post = Board.objects.get(id=request.GET['id'])
    content = {'post' : post}
    return render( request, 'board/view.html',content)




# # 수정, 삭제 혼자 실습
# # Board 내용 삭제코드
# def deleteboard( request ) :
#     del_board = Board.objects.get(id = request.GET['boardNum'])
#     del_board.delete()

#     return HttpResponseRedirect(reverse('list'))

# # Board를 수정하려는 페이지에 이전 Board내용 띄우기
# def amendboard( request ) :
#     pre_rows = Board.objects.get(id = request.GET['boardNum'])
#     pre_contents = {'pre_contents' : pre_rows} 
#     return render(request, 'board/amend.html', pre_contents)

# # Board수정 내용 list에 반영하기
# def re_create( request ):
#     pre_boards = Board.objects.get(id = request.POST['boardNum'])
#     pre_boards.createDate = request.POST['createDate']
#     pre_boards.writer = request.POST['user']
#     pre_boards.subject = request.POST['title']
#     pre_boards.content = request.POST['content']
#     pre_boards.save()
#     #dpre_board.update()

#     return HttpResponseRedirect(reverse('list'))


# # 게시판 확인
# def confirmboard(request):
#     pre_rows = Board.objects.filter(id = request.GET['boardNum'])
#     pre_contents = {'pre_contents' : pre_rows} 
#     return render(request, 'board/confirm.html', pre_contents)

# # 확인 후 다시 list로 돌아가기
# def back(request):
#     return HttpResponseRedirect(reverse('list'))