import uuid

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import os
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


# import notes
# from django_notes import settings


def get_attachment_path(instance, filename):
    user_id = instance.user.id
    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    return os.path.join('attachments', str(user_id), year, month, filename)


class TagManager(models.Manager):
    pass


class UserProfile(models.Model):
    db_table = 'notes_user'
    objects = TagManager()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    telegram = models.CharField(max_length=50, null=True, default=None)
    is_verified_email = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Note(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, default='')
    image = models.ImageField(upload_to=get_attachment_path, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, D: {self.deleted}'


class Content(models.Model):
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    order = models.IntegerField()
    content_type = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    objects = TagManager()
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
    tag = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.tag


class EmailVerification(models.Model):
    objects = TagManager()
    code = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        message = 'Для подтверждения учётной записи {} перейдите по ссылке: \n{}'.format(
            self.user.username,
            verification_link
        )
        html_message = 'Для подтверждения учётной записи <b>{}</b> <a href="{}"> перейдите по ссылке </a>'.format(
            self.user.username,
            verification_link
        )
        print(f'User{settings.EMAIL_HOST_USER} -> {settings.EMAIL_HOST_PASSWORD}')
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(self.user.email, ),
            fail_silently=False,
            auth_user=settings.EMAIL_HOST_USER,
            auth_password=settings.EMAIL_HOST_PASSWORD
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
