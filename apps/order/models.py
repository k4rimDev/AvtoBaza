from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.order import tasks

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
    
    @property
    def total_price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity

    def __str__(self):
        try:
            return self.product.name
        except:
            return self.order.transaction_id

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
    
    address = models.TextField(verbose_name="Ünvan", null=True, blank=True)
    
    status = models.CharField(max_length=50, choices=constants.ORDER_STATUS, 
                              default="pending", verbose_name="Sifarişin statusu")

    comment = models.TextField(null=True, blank=True, verbose_name="Şərh?")

    is_viewed = models.BooleanField(default=False, verbose_name="Sifarişə baxılıb?")

    @property
    def total_price(self) -> float:
        price = 0
        for i in self.orderitems.all():
            price += i.total_price
        
        return price
    
    @property
    def total_done_amount(self) -> float:
        price = 0
        for i in self.orderitems.all():
            if i.status == "done" or "send":
                price += i.total_price
        return price
    
    @property
    def total_done_count(self) -> float:
        quantity = 0
        for i in self.orderitems.all():
            if i.status == "done" or "send":
                quantity += i.quantity
        return quantity

    def __str__(self) -> str:
        return "{user}'in sifarişi".format(user=self.user.email)
    
    def save(self, *args, **kwargs) -> None:
        self.address = self.user.address
        tasks.delayed_change_status.apply_async(args=[self.id], countdown=10)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Sifariş')
        verbose_name_plural = _('Sifarişlər')
        ordering=["-created_at"]

class CustomManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        for i in objs:
            OrderItems.objects.create(
                order=i.order,
                product=i.product,
                quantity=i.quantity
            )
        return super(CustomManager, self).bulk_create(objs,**kwargs)

class OrderItems(DateMixin):

    transaction_id = models.CharField(max_length=12, unique=True,
                                      null=True, blank=True,
                                      verbose_name="Sifarişin kodu")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems",
                                        verbose_name="Sifariş")
    
    product = models.ForeignKey(pm.Product, related_name="orderitems", 
                                on_delete=models.CASCADE, verbose_name="Məhsul",
                                null=True, blank=True)
    
    status = models.CharField(max_length=50, choices=constants.ORDER_STATUS, 
                              default="pending", verbose_name="Sifarişin statusu")
    
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Məhsulun sayı")


    objects = CustomManager()

    @property
    def total_price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity

    def __str__(self):
        try:
            return self.product.name
        except:
            return self.order.transaction_id
    
    class Meta:
        verbose_name = "Sifarişin detalı"
        verbose_name_plural = "Sifarişin detalı"
        ordering=["-created_at"]

class UserAccount(DateMixin):
    
    user = models.ForeignKey(bm.MyUser, related_name="user_account", on_delete=models.CASCADE,
                             verbose_name="İstifadəçi", unique=True, db_index=True)
    
    total_payment = models.FloatField(default=0, verbose_name="Ümumi ödəniş")
    total_sale = models.FloatField(default=0, verbose_name="Ümumi satış")
    total_balance = models.FloatField(default=0, verbose_name="Ümumi qalıq")
    total_product_count = models.PositiveIntegerField(default=1, verbose_name="Ümumi məhsul sayı")

    def __str__(self) -> str:
        return "{user}'in səbəti".format(user=self.user.email)
    
    def save(self, *args, **kwargs) -> None:
        self.total_balance = self.total_sale - self.total_payment
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('İstifadəçinin satış üzrə cari hesabı')
        verbose_name_plural = _('İstifadəçilərin satış üzrə cari hesabı')
