from django.db import models
from django.utils.translation import gettext_lazy as _

# Image
from imagekit.models import ImageSpecField
from pilkit.processors import TrimBorderColor, Adjust

# Utils
from apps.utils.watermark import Watermark
from apps.utils.services import logo_dir_path, compress_image
from apps.utils.unique_slug import unique_slug_generator_with_name as us_name
from apps.utils.validators import max_image_size
from apps.utils.mixins import DateMixin, SlugMixin


class Brand(DateMixin, SlugMixin):
    brand_code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self.name)
        return super().save()
    
    class Meta:
        verbose_name = _('Marka')
        verbose_name_plural = _('Marka')

class BrandGroup(DateMixin, SlugMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self.name)
        return super().save()
    
    class Meta:
        verbose_name = _('Qrup')
        verbose_name_plural = _('Qruplar')

class Discount(DateMixin):
    discount_percent = models.PositiveSmallIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percent}% endirim"
    
    class Meta:
        verbose_name = _('Endirim')
        verbose_name_plural = _('Endirimlər')

class Product(DateMixin, SlugMixin):

    STOCK_STATUS = (
        ("yes", "Var"),
        ("no", "Yox")
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    brand = models.ManyToManyField(Brand, null=True, blank=True, 
                                   related_name="products")
    
    group = models.ForeignKey(BrandGroup, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="products")
    
    price = models.FloatField(default=0)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name="products")
    
    stock_status = models.CharField(max_length=10, choices=STOCK_STATUS)
    stock_count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self.name)
        # for image in self.images.all():
        #     image = compress_image(image)                
        #     image.save()    
        return super().save()

    @property
    def discount_price(self):
        if self.discount:
            return self.price * (100 - self.discount.discount_percent) / 100
        return None
    
    class Meta:
        verbose_name = _('Məhsul')
        verbose_name_plural = _('Məhsullar')

class ProductImage(DateMixin):
    watermarked_image = ImageSpecField(processors=[Watermark(), TrimBorderColor(),
                                        Adjust(contrast=1.2, sharpness=1.1), ], source='image',
                                       format='JPEG', options={'quality': 90})
    
    image = models.ImageField('Image', upload_to=logo_dir_path, null=True, blank=True, validators=[max_image_size])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='images')

    class Meta:
        verbose_name = _('Məhsul şəkili')
        verbose_name_plural = _('Məhsullar şəkilləri')

    def __str__(self) -> str:
        return f"{self.product.name}-un {self.id}-cı şəkili"
    
    def save(self, *args, **kwargs):                
        new_image = compress_image(self.image)                
        self.image = new_image            
        super().save(*args, **kwargs)
