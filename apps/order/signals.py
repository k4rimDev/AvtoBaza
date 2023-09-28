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
    if instance.status == "done" or instance.status == "send":

        models.OrderItems.objects.filter(pk=instance.pk).update(
            transaction_id=services.generate_unique_id_order_items(instance.id)
        )

        # balance = am.Balance.objects.get(
        #     user=instance.order.user
        # )
        # balance.balance -= instance.total_price
        # balance.save()

        user_account, _ = models.UserAccount.objects.get_or_create(
            user = instance.order.user
        )

        user_balance = am.UserBalance.objects.create(
            user=instance.order.user,
            balance = instance.total_price,
            order=instance,
            description=f"{instance.product.name} məhsulunun realizasiyası",
            transaction_type="outcome"
        )

        models.UserAccount.objects.filter(pk=user_account.pk).update(
            total_balance = (user_balance.remain_balance + instance.total_price)
        )

@receiver(pre_save, sender=models.OrderItems)
def check_order_item_status(sender, instance, **kwargs):
    if instance.pk:
        status = instance.status
        if status == "returned":
            am.UserBalance.objects.create(
                user=instance.order.user,
                balance=-instance.total_price,
                order=instance,
                description=f"Alıcıdan {instance.product.name} məhsulunun geri qaytarılması",
                transaction_type="income"
            )

            account, _ = models.UserAccount.objects.get_or_create(
                user=instance.order.user
            )

            updated_sale = account.total_sale - instance.total_price
            updated_quantity = account.total_product_count - instance.quantity

            models.UserAccount.objects.filter(pk=account.pk).update(
                total_sale = updated_sale,
                total_product_count = updated_quantity
            )

@receiver(pre_save, sender=models.UserAccount)
def change_user_remain_balance(sender, instance, **kwargs):
    if instance.pk:
        previous_balance = models.UserAccount.objects.get(
            pk=instance.pk
        ).total_payment

        if instance.total_payment > previous_balance:
            am.UserBalance.objects.create(
                user=instance.user,
                balance = (instance.total_payment - previous_balance),
                description = "Kassaya mədaxil orderi",
                remain_balance = (instance.total_sale - instance.total_payment),
                transaction_type = "income"
            )
