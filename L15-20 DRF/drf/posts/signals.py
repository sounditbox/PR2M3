import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from posts.models import Article

User = get_user_model()

logging.basicConfig(level=logging.INFO, filename='log.log')
logger = logging.getLogger(__name__)


@receiver(user_logged_in, sender=User)
def user_logged_in(sender, user, request, **kwargs):
    logger.info(f'User {user} logged in')


@receiver(user_logged_out, sender=User)
def user_logged_out(sender, user, request, **kwargs):
    logger.info(f'User {user} logged out')


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    if created:
        logger.info(f'Article {instance} created by {instance.author}')
    else:
        logger.info(f'Article {instance} updated by {instance.author}')


@receiver(post_save, sender=User)
def user_post_save(sender, instance: User, created, **kwargs):
    if created:
        logger.info(f'User {instance} created')

        group = Group.objects.get(name='Author')
        group.user_set.add(instance)
        send_mail(
            subject='Добро пожаловать в Магазин Котиков!',
            message=f'Привет, {instance.username}! Рады видеть тебя среди любителей котиков!',
            from_email='no-reply@catshop.com',
            recipient_list=[instance.email],
        )
        # Group.objects.get('Author').user_set.add(instance)

