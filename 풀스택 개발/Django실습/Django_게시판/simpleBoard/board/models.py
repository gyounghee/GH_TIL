from abc import update_abstractmethods
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ORM(Object Relation Mapping)
class Board( models.Model ) :
    user = models.ForeignKey(User, on_delete = models.CASCADE)  # user가 삭제되면 해당 user 테이블도 함께 삭제하는 코드추가
    createDate = models.DateField()
    # writer = models.CharField(max_length = 128)  
    subject = models.CharField(max_length = 255)
    content = models.TextField()  # TextField는 가변타입
