import time

from celery import shared_task

from apps.order import models

@shared_task
def delayed_change_status(instance_id):
    instance = models.Order.objects.get(pk=instance_id)
    
    time.sleep(5)

    is_done = False
    is_canceled = False
    is_pending = False
    for i in instance.orderitems.all():
        if i.status == "done" or i.status == "send":
            is_done = True
        elif i.status == "canceled" or i.status == "returned":
            is_canceled = True
        elif i.status == "is_pending":
            is_pending = True

    if is_done and (is_canceled or is_pending):
        instance.status = "partially send"

    elif is_done and not is_canceled and not is_pending:
        instance.status = "done"

    if is_canceled and not is_done and not is_pending:
        instance.status = "canceled"

    instance.save()