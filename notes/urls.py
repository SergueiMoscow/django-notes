from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('tags/', views.tags, name='tags'),
]