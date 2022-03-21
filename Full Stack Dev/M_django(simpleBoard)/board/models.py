from django.db import models

from django.contrib.auth.models import User

# Create your models here.
# ORM(Object Relataion mapping)

class Board( models.Model ):
  # on_delete 속성은 ForeignKey 로 연결되는 모델(User)의 데이터가 삭제될 경우 해당 ForeignKey 필드의 값을 어떻게 할 지에 대한 설정
  # CASCADE는 연결된 모델(User)의 인스턴스가 삭제되면 해당 인스턴스를 ForeignKey로 연결한 Article의 인스턴스도 같이 삭제
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  createDate = models.DateField()
  # user = models.CharField(max_length=128)
  subject = models.CharField(max_length=255)
  content = models.TextField()