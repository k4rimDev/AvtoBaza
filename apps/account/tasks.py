from django.utils import timezone
from django.contrib.auth import get_user_model

from celery import shared_task


User = get_user_model()

@shared_task
def check_user_last_login_time():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)
    expired_announcements = User.objects.filter(last_login__lte=one_month_ago)
    expired_announcements.update(is_active=False)
