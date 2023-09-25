from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import ValidationError

from apps.order import models as om
from apps.product import models as pm
from apps.account import models as am
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
        fields = ('id', 'product', 'product_id', 'quantity') # product_id for add item to cart

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
            return ps.ProductSerializer(obj.product, context=self.context).data

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
    
class OrderSerializer(serializers.ModelSerializer):
    ids = serializers.ListField(required=False)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = om.Order
        fields = ("transaction_id", "status", "comment",
                  "created_at", "ids")
        
    def create(self, validated_data):
        ids = validated_data.pop("ids")
        instance = om.Order.objects.create(
            user=self.context["user"],
            comment=validated_data.get("comment", None)
        )

        return instance
        
    def get_created_at(self, obj):
        try:
            formatted_time = datetime.strftime(
            obj.created_at,
                "%Y-%m-%d %H:%M:%S"
            )
            return formatted_time
        except:
            return None
        
    def validate_ids(self, field):
        if not len(field) > 0:
            raise ValidationError({"message": "Ids must added"})
        for i in field:
            if not om.CartItem.objects.filter(id=i).exists():
                raise ValidationError({"message": "Id not exists"})
        return field
    
class OrderItemCreateSerializer(serializers.ModelSerializer):
    ids = serializers.ListField(required=False)
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = om.OrderItems
        fields = ("status", "created_at", "ids")
        
    def create(self, validated_data):
        ids = validated_data.pop('ids')
        instance_list = []
        order_instance = self.context.get('order')

        if ids and len(ids) > 0:
            for i in ids:
                cart_item = om.CartItem.objects.filter(id=i)
                if cart_item.exists():
                    instance_product = pm.Product.objects.filter(id=cart_item[0].product.id).first()
                    instance_quantity = cart_item[0].quantity
                    om.OrderItems.objects.create(order=order_instance, product=instance_product, quantity=instance_quantity)
                    user_tracking = am.UserTracking.objects.create(
                        user=self.context["user"]
                    )
                    user_tracking.description = f"""
                        {self.context["user"]} istifadəçi {instance_product} məhsulunu sifariş verdi.
                    """
                    
                    user_tracking.save()

                    cart_item.delete()

            return instance_list
        else:
            raise serializers.ValidationError({"message": "Cart items Id's must be added"})
        
    def get_created_at(self, obj):
        try:
            formatted_time = datetime.strftime(
            obj.created_at,
                "%Y-%m-%d %H:%M:%S"
            )
            return formatted_time
        except:
            return None
        
    def validate_ids(self, field):
        if not len(field) > 0:
            raise ValidationError({"message": "Ids must added"})
        for i in field:
            if not om.CartItem.objects.filter(id=i).exists():
                raise ValidationError({"message": "Id not exists"})
        return field
 
class OrderItemSerializer(serializers.ModelSerializer):
    product = ps.ProductSerializer()
    class Meta:
        model = om.OrderItems
        fields = ("id", "status", "quantity", "product")     

class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = om.Order
        fields = ("transaction_id", "status", "comment",
                  "created_at", "items")
        
    def get_items(self, obj):
        items = obj.orderitems.all()
        serializers = OrderItemSerializer(items, many=True, context=self.context)
        return serializers.data
    
    def get_created_at(self, obj):
        formatted_time = datetime.strftime(
            obj.created_at,
            "%Y-%m-%d %H:%M:%S"
        )
        return formatted_time
