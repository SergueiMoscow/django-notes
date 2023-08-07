from django.contrib import admin

from .models import Note, Tag, EmailVerification

admin.site.site_header = 'Мои заметки'
# admin.site.register(Note)


class TagInline(admin.TabularInline):
    model = Tag


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    inlines = (TagInline, )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created_at', )
