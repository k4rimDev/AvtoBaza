from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.base_user import models as bm

from apps.utils.mixins import DateMixin


class UserTracking(DateMixin):
    ...

class UserBalance(DateMixin):
    user = models.ForeignKey(bm.MyUser, related_name="balance", on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", unique=True, db_index=True)
    
    balance = models.FloatField(default=0, verbose_name="Balans")

    def __str__(self):
        return "{user}'in balansı ----- {balance}".format(user=self.user.email, balance=self.balance)
    
    class Meta:
        verbose_name = _('İstifadəçi balansı')
        verbose_name_plural = _('İstifadəçi balansı')
