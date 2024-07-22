from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, Profile
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Post)
def notify_post_creation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Post Created',
            f'A new post titled "{instance.title}" has been created by {instance.author.username}.',
            settings.DEFAULT_FROM_EMAIL,
            [instance.author.email],
            fail_silently=False,
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
