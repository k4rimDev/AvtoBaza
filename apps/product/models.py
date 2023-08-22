from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        self.slug = slugify(self.name)
        return super().save()
    
    class Meta:
        verbose_name = _('Marka')
        verbose_name_plural = _('Marka')

class BrandGroup(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        self.slug = slugify(self.name)
        return super().save()
    
    class Meta:
        verbose_name = _('Qrup')
        verbose_name_plural = _('Qruplar')

class Discount(models.Model):
    discount_percent = models.PositiveSmallIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percent}% endirim"
    
    class Meta:
        verbose_name = _('Endirim')
        verbose_name_plural = _('Endirimlər')

class Product(models.Model):

    STOCK_STATUS = (
        ("yes", "Var"),
        ("no", "Yox")
    )

    slug = models.SlugField(unique=True, db_index=True)

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    brand_code = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="products")
    
    group = models.ForeignKey(BrandGroup, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="products")
    
    price = models.FloatField(default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name="products")
    
    stock = models.CharField(max_length=20, choices=STOCK_STATUS)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        self.slug = slugify(self.name)
        return super().save()
    
    @property
    def discount_price(self):
        if self.discount:
            return self.price * (100 - self.discount.discount_percent) / 100
        return None
    
    class Meta:
        verbose_name = _('Məhsul')
        verbose_name_plural = _('Məhsullar')
