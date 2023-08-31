from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.product.models import Product
from apps.base_user.models import User


class MainData(models.Model):
    logo = models.FileField(upload_to="core/logo")
    favicon = models.FileField(upload_to="core/favicon")

    def __str__(self):
        return "Əsas məlumatlar"
    class Meta:
        verbose_name = _('Əsas məlumatlar')
        verbose_name_plural = _('Əsas məlumatlar')

class BrandNumber(models.Model):
    brand_logo = models.FileField(upload_to="core/brand-logo")
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} -- {self.number}"
    
    class Meta:
        verbose_name = _('Marka nomreleri')
        verbose_name_plural = _('Marka nomreleri')

class CampaignText(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = _('Kampaniya məlumatları')
        verbose_name_plural = _('Kampaniya məlumatları')

class SuggestionComplaints(models.Model):
    text = models.TextField(verbose_name="Təklif və Şikayət:")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name="suggestions",
                             verbose_name="İstifadəçi:")

    def __str__(self):
        return f"İstifadəçinin emaili - {str(self.user.email)}"
    
    class Meta:
        verbose_name = _('Təklif və şikayətlər')
        verbose_name_plural = _('Təklif və şikayətlər')

class Slider(models.Model):
    slug = models.SlugField(unique=True, db_index=True)
    image = models.FileField(upload_to="core/slider")
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    order_count = models.PositiveSmallIntegerField(null=True, blank=True)
    products = models.ManyToManyField(Product, null=True,
                                     blank=True, related_name="sliders")

    def __str__(self):
        return self.title
    
    def save(self) -> None:
        self.slug = slugify(self.title)
        return super().save()
    
    class Meta:
        verbose_name = _('Slayder')
        verbose_name_plural = _('Slayder')
