from rest_framework import serializers

from apps.order import models as om
from apps.product import models as pm
from apps.product.api import serializers as ps


class UpdateCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    cartid = serializers.IntegerField()

class DeleteCartSerializer(serializers.Serializer):
    cartid = serializers.IntegerField()

class ProductIdSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=pm.Product.objects.all())

class CartSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=pm.Product.objects.all(), required=False)
    product = serializers.SerializerMethodField()

    class Meta:
        model = om.CartItem
        fields = ('id', 'product', 'product_id', 'quantity')

    def validate_product_id(self, value):
        request = self.context.get('request')
        if request and request.method == "POST":
            product = value.id
            if not product:
                raise serializers.ValidationError({"message": 'Product ID is required!'})
            if not pm.Product.objects.filter(id=product).exists():
                raise serializers.ValidationError({"message": 'Product ID is not valid!'})
        return value
    
    def get_product(self, obj):
        request = self.context.get('request')
        if request and request.method == 'GET':
            return ps.ProductSerializer(obj.product).data

    def create(self, validated_data):
        cart = self.context["cart"]
        product_data = validated_data.pop('product_id')
        instance, _created = om.CartItem.objects.get_or_create(cart=cart, product=product_data)
        instance.quantity = validated_data.pop('quantity')
        instance.save()
        return instance

    def update(self, instance, validated_data):
        request = self.context.get('request')
        quantity = self.context.get('quantity', None)

        if request and request.method == 'PATCH':
            validated_data.pop('product', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if quantity is not None:
            instance.quantity = quantity

        instance.save()
        return instance
    