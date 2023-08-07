import os
import django

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_notes.settings'

# Загружаем и настраиваем Django
django.setup()
