from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('tags/', views.tags, name='tags'),
    path('note/<int:note_id>/', views.show, name='show'),
    path('list_notes/', views.list_notes, name='list_notes'),
]