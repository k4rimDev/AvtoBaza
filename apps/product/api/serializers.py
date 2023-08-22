from rest_framework import serializers

from apps.product import models


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ('id', 'slug', 'name')
        
class BrandGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BrandGroup
        fields = ('id', 'slug', 'name')

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Discount
        fields = ('id', 'discount_percent')

class ProductSerializer(serializers.ModelSerializer):
    
    group = BrandGroupSerializer()
    brand = BrandSerializer()
    discount = DiscountSerializer()

    class Meta:
        model = models.Product
        fields = ('id', 'slug', 'code', 'name', 'brand_code', 
                  'brand', 'group', 'price', 'discount',
                  'stock', 'discount_price')
