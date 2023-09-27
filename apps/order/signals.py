from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.order import models
from apps.account import models as am

from apps.utils import services


@receiver(post_save, sender=models.Order)
def generate_transaction_id(sender, instance, created, **kwargs):
    if created:
        instance.transaction_id = services.generate_unique_id(instance.id)
        instance.save()
    else:
        if instance.status == "done" or "partially done":
            account, _ = models.UserAccount.objects.get_or_create(
                user=instance.user
            )
            
            account.total_sale += instance.total_done_amount
            account.total_product_count += instance.total_done_count

            account.save()

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

@receiver(pre_save, sender=models.OrderItems)
def check_order_item_status(sender, instance, **kwargs):
    if instance.pk:
        status = instance.status
        if status == "returned":
            am.UserBalance.objects.create(
                user=instance.order.user,
                balance = instance.total_price,
                order=instance,
                description=f"Alıcıdan {instance.product.name} məhsulunun geri qaytarılması",
                transaction_type="income"
            )

            account, _ = models.UserAccount.objects.get_or_create(
                user=instance.order.user
            )

            updated_balance = account.total_balance - instance.total_price

            models.UserAccount.objects.filter(pk=account.pk).update(
                total_balance = updated_balance
            )
