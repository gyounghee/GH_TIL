from django.urls import path
from myapp import views

urlpatterns = [
    path('',views.index),
    path('create/',views.create),
    path('read/<id>/',views.read),    # <> : 가변적인 즉, 바뀔 수 있는 값이 올 떄 
    path('delete/',views.delete),
    path('update/<id>/',views.update)
]
