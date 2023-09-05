from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from apps.product.models import Product
from apps.base_user.models import User


class MainData(models.Model):
    logo = models.FileField(verbose_name="Əsas loqo", upload_to="core/logo")
    footer_logo = models.FileField(verbose_name="Aşağı hissədəki loqo", 
                                   upload_to="core/logo", 
                                   null=True, blank=True)
    
    hero_section_bg = models.FileField(verbose_name="Ana səhifədəki arxa fon şəkili", 
                                   upload_to="core/images", 
                                   null=True, blank=True)
    
    favicon = models.FileField(verbose_name="Favikon", upload_to="core/favicon")

    phone_number = models.CharField(max_length=30, 
                                    verbose_name="Bizimlə Əlaqə nömrəsi",
                                    null=True, blank=True)

    def __str__(self):
        return "Əsas məlumatlar"
    class Meta:
        verbose_name = _('Əsas məlumatlar')
        verbose_name_plural = _('Əsas məlumatlar')

class AboutUs(models.Model):
    title = models.CharField(max_length=200, 
                                    verbose_name="Başlıq",
                                    null=True, blank=True)
    
    text = RichTextField(verbose_name="Ətraflı Mətn", help_text="Şəkil, link və s. əlavə oluna bilər.")

    def __str__(self):
        if self.title:
            return self.title
        return "Haqqımızda"
    
    class Meta:
        verbose_name = _('Haqqımızda')
        verbose_name_plural = _('Haqqımızda')  

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
