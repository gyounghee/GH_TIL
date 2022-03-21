from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='list'),
    path('write/', views.write),
    path('create/', views.create),
    path('delete/', views.delete), 
    path('update/', views.update),
    path('modify/', views.modify),
    path('view/', views.view),

]