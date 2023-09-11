from django.db import models


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,
                                      verbose_name="Yaranma tarixi")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True,
                                      verbose_name="Güncəllənmə tarixi")

    class Meta:
        abstract = True

class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, editable=False, db_index=True)

    class Meta:
        abstract = True
