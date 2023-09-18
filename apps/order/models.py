from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.mixins import DateMixin

from apps.base_user import models as bm
from apps.product import models as pm

from apps.utils import constants


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

class Order(DateMixin):
    transaction_id = models.CharField(max_length=15, unique=True,
                                      null=True, blank=True,
                                      verbose_name="Sifarişin kodu")

    user = models.ForeignKey(bm.User, on_delete=models.CASCADE, 
                             related_name="orders", verbose_name="İstifadəçi")
    
    status = models.CharField(max_length=50, choices=constants.ORDER_STATUS, 
                              default="pending", verbose_name="Sifarişin statusu")

    comment = models.TextField(null=True, blank=True, verbose_name="Şərh?")

    is_viewed = models.BooleanField(default=False, verbose_name="Sifarişə baxılıb?")

    def __str__(self):
        return "{user}'in sifarişi".format(user=self.user.email)

    class Meta:
        verbose_name = _('Sifariş')
        verbose_name_plural = _('Sifarişlər')

class OrderItems(DateMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems",
                                        verbose_name="Sifariş")
    
    product = models.ForeignKey(pm.Product, related_name="orderitems", 
                                on_delete=models.CASCADE, verbose_name="Məhsul",
                                null=True, blank=True)
    
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Məhsulun sayı")

    def __str__(self):
        return self.product.name
    
    class Meta:
        verbose_name = "Sifarişin detalı"
        verbose_name_plural = "Sifarişin detalı"
