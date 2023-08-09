import uuid
from datetime import timedelta

from celery import shared_task
from django.contrib.auth.models import User
from django.utils.timezone import now

from notes.models import EmailVerification


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=24)
    email_verification = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    email_verification.save()
    email_verification.send_verification_email()
