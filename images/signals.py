from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.user_like.through)
def user_like_changed(sender, instance, **kwargs):
    '''A reciever function to update the number of total likes per image after each action'''
    '''This function works syncronous, might consider caching, asynronous calls, or even cron jobs
    to populate it'''
    instance.total_likes = instance.user_like.count()
    instance.save()