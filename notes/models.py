from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import os


def get_attachment_path(instance, filename):
    user_id = instance.user.id
    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    return os.path.join('attachments', str(user_id), year, month, filename)


class TagManager(models.Manager):
    pass


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


class UserProfile(models.Model):
    objects = TagManager()
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True, upload_to="images/profile/")

    def __str__(self):
        return str(self.user)
