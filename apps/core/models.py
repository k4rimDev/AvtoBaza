from django.db import models

from django.utils.translation import gettext_lazy as _


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

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = _('Kampaniya məlumatları')
        verbose_name_plural = _('Kampaniya məlumatları')

class Slider(models.Model):
    image = models.FileField(upload_to="core/slider")
