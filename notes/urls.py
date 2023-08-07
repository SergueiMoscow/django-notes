from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='note_new'),
    path('tags/', views.tags, name='tags_list'),
    path('note/<int:note_id>/', views.show, name='note_show'),
    path('note/<int:note_id>/edit', views.edit, name='note_edit'),
    path('note/<int:note_id>/delete', views.delete, name='note_delete'),
    path('list_notes/', views.list_notes, name='notes_list'),
]
