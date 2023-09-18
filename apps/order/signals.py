from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.order import models
from apps.utils import services


@receiver(post_save, sender=models.Order)
def generate_transaction_id(sender, instance, created, **kwargs):
    print("sdfs")
    if created:
        instance.transaction_id = services.generate_unique_id(instance.id)
        instance.save()
