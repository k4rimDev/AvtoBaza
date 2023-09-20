from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.order import models
from apps.account import models as am

from apps.utils import services


@receiver(post_save, sender=models.Order)
def generate_transaction_id(sender, instance, created, **kwargs):
    if created:
        instance.transaction_id = services.generate_unique_id(instance.id)
        instance.save()

@receiver(post_save, sender=models.OrderItems)
def update_balance(sender, instance, created, **kwargs):
    if created:
        
        instance.transaction_id = services.generate_unique_id_order_items(instance.id)
        instance.save()

        balance = am.Balance.objects.get(
            user=instance.order.user
        )
        balance.balance -= instance.total_price
        balance.save()

        user_balance = am.UserBalance.objects.create(
            user=instance.order.user,
            balance = instance.total_price,
            order=instance,
            description=f"{instance.product.name} məhsulunun realizasiyası",
            transaction_type="outcome"
        )

        user_balance.remain_balance = balance.balance
        user_balance.save()
        