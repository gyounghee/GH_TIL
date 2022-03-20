from django.db import models

# Create your models here.
# 클래스의 이름 = 모델(테이블)의 이름
class Todo(models.Model):
    # Todo 테이블에 content라는 컬럼 생성
    # content 타입은 문자 타입이며, 최대 길이가 255byte
    content = models.CharField(max_length = 255)  