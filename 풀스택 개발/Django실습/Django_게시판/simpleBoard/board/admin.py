from django.contrib import admin
from .models import Board  # 등록할 모델을 가져옴

# Register your models here.

class BoardAdmin( admin.ModelAdmin ) : # admin에 있는 ModelAdmin을 상속받아서 재정의 
    # 관리자 페이지에서 화면에 보여지는 목록
    list_display = ('createDate', 'user' ,'subject')  # 튜플 또는 리스트로 만들어주면 됨

    # 링크 새로 정의 가능  (default : 리스트에서 디테일뷰로 넘어갈떄 날짜선택)
    # 제목을 클릭해서 상세페이지로 이동하도록 재정의
    list_display_links = ['subject'] 

admin.site.register(Board, BoardAdmin)  # admin을 이용하여 모델 등록