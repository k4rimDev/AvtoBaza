from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.base_user import models as bm

from apps.utils.mixins import DateMixin
from apps.utils import constants


class UserTracking(DateMixin):
    user = models.ForeignKey(bm.MyUser, on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", db_index=True,
                             related_name="usertracking")
    
    description = models.TextField(verbose_name="Ətraflı")

    def __str__(self):
        return "{user}'in ----- {desc}".format(user=self.user.email, desc=self.description)
    
    class Meta:
        verbose_name = _('İstifadəçi aktivliyi')
        verbose_name_plural = _('İstifadəçi aktivliyi')

class Balance(DateMixin):
    user = models.OneToOneField(bm.MyUser, on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", db_index=True, 
                             related_name="balances")
    
    balance = models.FloatField(default=0, verbose_name="Balans")

    def __str__(self):
        return "{user}'in balansı ----- {balance}".format(user=self.user.username, balance=self.balance)
    
    class Meta:
        verbose_name = _('İstifadəçi balansı')
        verbose_name_plural = _('İstifadəçilərin balansı')
        ordering = ["-created_at"]

class UserBalance(DateMixin):
    user = models.ForeignKey(bm.MyUser, on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", db_index=True, 
                             related_name="userbalances")
    
    balance = models.FloatField(default=0, verbose_name="Balans")
    remain_balance = models.FloatField(default=0, verbose_name="Qalıq balans")
    
    description = models.CharField(max_length=100, verbose_name="Ətraflı", null=True, blank=True)

    transaction_type = models.CharField(max_length=50, default="Mədaxil",
                                        choices=constants.TRANSACTION_TYPE,
                                        null=True, blank=True,
                                        verbose_name="Mədaxil & Məxaric")
    
    def __str__(self):
        return "{user}'in balansı ----- {balance}".format(user=self.user.email, balance=self.balance)
    
    class Meta:
        verbose_name = _('İstifadəçi cari hesabı')
        verbose_name_plural = _('İstifadəçilərin cari hesabı')
        ordering = ["-created_at"]
