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
    thumb_images = serializers.SerializerMethodField()
    
    group = BrandGroupSerializer()
    brand = BrandSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'slug', 'code', 'name', 'brand', 
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

class PriceComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Complaint
        fields = ("price", "product", "company")

    def validate(self, attrs):
        text = attrs.get('company')
        if not text:
            raise serializers.ValidationError({"message": 'Company is required'})
        
        price = float(attrs.get('price'))
        if price < 0:
            raise serializers.ValidationError({"message": 'Price can\'t less than zero'})
        
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context["request"].user
        instance = models.Complaint.objects.create(
            user=user,
            **validated_data
        )

        return instance
