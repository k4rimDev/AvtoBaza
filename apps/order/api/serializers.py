from rest_framework import serializers

from apps.order import models as om
from apps.product import models as pm
from apps.product.api import serializers as ps


class CartSerializer(serializers.ModelSerializer):
    product = ps.ProductSerializer()
    class Meta:
        model = om.CartItem
        fields = ('id', 'product', 'quantity')

    def validate(self, attrs):
        print("kerim is here")
        product = attrs.get('product')
        if not pm.Product.objects.filter(id=product).exists():
            raise serializers.ValidationError({"message": 'Product slug is not valid!'})
        return super().validate(attrs)

    def create(self, validated_data):
        cart = self.context["cart"]
        print("sdfsfsf")
        instance = om.CartItem.objects.create(
            cart=cart
            **validated_data
        )

        return instance
    
    def update(self, instance, validated_data):
        quantity = self.context["quantity"]
        
        instance.quantity=quantity
        return instance
        