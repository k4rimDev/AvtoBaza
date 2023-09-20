from django.db import models
from django.utils.translation import gettext_lazy as _

# Image
from imagekit.models import ImageSpecField
from pilkit.processors import TrimBorderColor, Adjust

from apps.base_user.models import MyUser

# Utils
from apps.utils.watermark import Watermark
from apps.utils.services import logo_dir_path, compress_image
from apps.utils.unique_slug import unique_slug_generator_with_name as us_name
from apps.utils.validators import max_image_size
from apps.utils.mixins import DateMixin, SlugMixin


class Brand(DateMixin, SlugMixin):
    brand_code = models.CharField(max_length=20, verbose_name="Markanın kodu")
    name = models.CharField(max_length=200, verbose_name="Markanın adı")

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self)
        return super().save()
    
    class Meta:
        verbose_name = _('Marka')
        verbose_name_plural = _('Marka')
    
class BrandGroup(DateMixin, SlugMixin):
    name = models.CharField(max_length=200, verbose_name="Qrupun adı")

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self)
        return super().save()
    
    class Meta:
        verbose_name = _('Qrup')
        verbose_name_plural = _('Qruplar')

class Discount(DateMixin):
    discount_percent = models.PositiveSmallIntegerField(default=10, verbose_name="Endirim faizi",
                                                        help_text="Məs. 10% endirim")
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir?")

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

    name = models.CharField(max_length=200, verbose_name="Məhsulun adı", db_index=True)
    code = models.CharField(max_length=200, verbose_name="Məhsulun kodu", db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL,
                                null=True, blank=True, related_name="products",
                                verbose_name="Məhsulun markası")
    
    group = models.ForeignKey(BrandGroup, on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="products",
                              verbose_name="Məhsulun qrupu")
    
    price = models.FloatField(default=0, verbose_name="Məhsulun qiyməti")

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name="products",
                                 verbose_name="Məhsulun endirimi",
                                 help_text="Əgər məhsul endirimdədirsə endirim faizini seçin")
    
    stock_status = models.CharField(max_length=10, choices=STOCK_STATUS, 
                                    verbose_name="Məhsulun stok vəziyyəti")
    
    stock_count = models.PositiveIntegerField(default=1, verbose_name="Məhsulun stok sayı")

    def __str__(self):
        return self.name
    
    def save(self) -> None:
        if not self.slug:
            self.slug = us_name(self)
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
    
    image = models.ImageField(upload_to=logo_dir_path, null=True, blank=True, validators=[max_image_size],
                              verbose_name="Məhsulun şəkili")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True, related_name='images')

    class Meta:
        verbose_name = _('Məhsul şəkili')
        verbose_name_plural = _('Məhsullar şəkilləri')

    def __str__(self) -> str:
        return f"{self.product.name}-un {self.id}-cı şəkili"
    
    def save(self, *args, **kwargs):  
        if not self.id:       
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

class Complaint(DateMixin):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="complaints",
                             verbose_name="İstifadəçi")
    
    price = models.FloatField(default=0, verbose_name="Başqa yerdə olan qiymət")
    company = models.CharField(max_length=200, verbose_name="Şirkət adı")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="complaints",
                                verbose_name="Məhsul")

    def __str__(self):
        return f"Məhsul: {self.product.name} Başqa yerdə olan qiymət:{self.price}"
    
    class Meta:
        verbose_name = _('Qiymətə narazıçılıq edənlər')
        verbose_name_plural = _('Qiymətə narazıçılıq edənlər')

class PopUpSlider(DateMixin):
    image = models.FileField(upload_to="core/slider", verbose_name="Popup'ın şəkili")
    title = models.CharField(max_length=200, verbose_name="Popup'ın başlığı")
    description = models.TextField(verbose_name="Popup'ın mətni", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktivdir?")
    order_count = models.PositiveSmallIntegerField(null=True, blank=True, 
                                                   verbose_name="Popup'ın sıra nömrəsi")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="popupsliders", 
                              null=True, blank=True, verbose_name="Popup'ın aid olduğu brend",
                              help_text="Boş qala bilər")
    group = models.ForeignKey(BrandGroup, on_delete=models.CASCADE, related_name="popupsliders",
                              null=True, blank=True, verbose_name="Popup'ın aid olduğu qrup",
                              help_text="Boş qala bilər")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  
        if not self.id:       
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _('Popup Slayderı')
        verbose_name_plural = _('Popup Slayderı')

class DiscountInfo(DateMixin):
    text = models.TextField(verbose_name="Endirim haqqındakı tekst")

    def __str__(self):
        return self.text
    
    class Meta:
        verbose_name = _('Endirim haqqında məlumat')
        verbose_name_plural = _('Endirim haqqında məlumat')
