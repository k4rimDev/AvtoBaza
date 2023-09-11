from rest_framework import serializers

from easy_thumbnails.files import get_thumbnailer

from apps.product import models


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('id', 'slug', 'name', 'brand_code')
        
class BrandGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BrandGroup
        fields = ('id', 'slug', 'name')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent')

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('image_with_absolute_url')

    def image_with_absolute_url(self, obj):
        request = self.context.get('request')
        thumb = self.context.get('thumb')
        url = obj.watermarked_image.url
        if request:
            if thumb:
                options = {'size': (460, 343), 'crop': True, 'upscale': True}
                url = get_thumbnailer(obj.image).get_thumbnail(options).url
            return request.build_absolute_uri(url)
        return url
    class Meta:
        model = models.ProductImage
        fields = ('id', 'image')

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    brands = serializers.SerializerMethodField()
    thumb_images = serializers.SerializerMethodField()
    
    group = BrandGroupSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'slug', 'code', 'name', 'brands', 
                  'group', 'price', 'discount', 'stock_count',
                  'stock_status', 'discount_price', 'images', 
                  'thumb_images')
        
    def get_thumb_images(self, obj):
        self.context['thumb'] = True
        serializer = ProductImageSerializer(instance=obj.images, context=self.context, many=True)
        return serializer.data

    def get_images(self, obj):
        self.context['thumb'] = False
        serializer = ProductImageSerializer(instance=obj.images, context=self.context, many=True)
        return serializer.data
    
    def get_brands(self, obj):
        serializer = BrandSerializer(obj.brand.all(), many=True)
        return serializer.data
