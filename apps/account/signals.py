from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.base_user.models import MyUser
from apps.account import models


@receiver(post_save, sender=MyUser)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        models.Balance.objects.create(
            user=instance
        )

@receiver(pre_save, sender=models.Balance)
def update_user_activity(sender, instance, **kwargs):
    if instance.pk:
        original_balance = instance.balance
        old_balance = models.Balance.objects.filter(pk=instance.pk)
        if old_balance.exists:
            old_balance = old_balance.first()
            if original_balance - old_balance.balance > 0:
                user_balance = models.UserBalance.objects.create(
                    user=instance.user,
                    remain_balance = original_balance,
                    balance = original_balance - old_balance.balance,
                    description="Balansın artırılması",
                    transaction_type="income"
                )

                models.UserTracking.objects.create(
                    user=instance.user,
                    description = f"""
                        {instance.user} istifadəçinin balansı {original_balance - old_balance.balance}
                        qədər artırıldı.
                    """
                )

        else:
            models.UserBalance.objects.create(
                user=instance.user,
                balance = original_balance,
                remain_balance = original_balance,
                description="Hesabın yaradılması",
                transaction_type=""
            )
