from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins import DateMixin

from apps.base_user import models as bm
from apps.product import models as pm


class Cart(DateMixin):
    
    user = models.ForeignKey(bm.MyUser, related_name="cart", on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", unique=True, db_index=True)

    def __str__(self):
        return "{user}'in səbəti".format(user=self.user.email)
    
    class Meta:
        verbose_name = _('İstifadəçi səbəti')
        verbose_name_plural = _('İstifadəçi səbəti')

class CartItem(DateMixin):
    cart = models.ForeignKey(Cart, related_name="cartitems", 
                                on_delete=models.CASCADE, verbose_name="Səbət")
    
    product = models.ForeignKey(pm.Product, related_name="cartitems", 
                                on_delete=models.CASCADE, verbose_name="Məhsul")
    
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Məhsulun sayı")
    
    def __str__(self):
        return "{user}'in səbəti".format(user=self.cart.user.email)

    class Meta:
        verbose_name = _('İstifadəçi səbəti')
        verbose_name_plural = _('İstifadəçi səbəti')
