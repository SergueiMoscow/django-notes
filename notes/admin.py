from django.contrib import admin

from .models import Note

admin.site.site_header = 'Мои заметки'
admin.site.register(Note)
