# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
]
