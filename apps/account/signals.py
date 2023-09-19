from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.base_user.models import MyUser
from apps.account import models


@receiver(post_save, sender=MyUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        models.Balance.objects.create(
            user=instance
        )

@receiver(post_save, sender=models.Balance)
def update_user_activity(sender, instance, created, **kwargs):
    if created:
        models.UserBalance.objects.create(
            user=instance.user,
            balance = instance.balance
        )
