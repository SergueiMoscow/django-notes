import uuid
from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from notes.models import EmailVerification, UserProfile


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#         expiration = now() + timedelta(hours=24)
#         email_verification = EmailVerification.objects.create(code=uuid.uuid4(), user=instance, expiration=expiration)
#         email_verification.save()
#         email_verification.send_verification_email()
