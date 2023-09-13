from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.order import models
from apps.order.api import serializers

from apps.utils.permissions import CustomPermissionOnlyGetProducts


class CartAPIView(APIView):
    allowed_methods = ["GET", "POST", "HEAD", 
                       "PATCH", "DELETE", "OPTIONS"]
    
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]
    serializer_class = serializers.CartSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        cart, _created = models.Cart.objects.get_or_create(
            user=user
        )

        return Response(serializers.CartSerializer(cart.cartitems.all(), many=True, 
                                                   context={"request": request}).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="This is for add cart functionality API",
                         request_body=serializers.CartSerializer)
    def post(self, request, *args, **kwargs):
        user = request.user
        cart, _created = models.Cart.objects.get_or_create(
            user=user
        )
        serializer = serializers.CartSerializer(
                data=request.data, 
                context={'request': request, 'cart': cart}
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description="This is for delete cart functionality API",
                         request_body=serializers.DeleteCartSerializer)
    def delete(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated!"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        cart, _created = models.Cart.objects.get_or_create(
            user=user
        )
        cart_id = request.data["cartid"]
        cart_items = models.CartItem.objects.filter(
            cart=cart,
            id=cart_id
        )

        if not cart_items.exists():
            return Response({"message": "Cart item not exists!"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_items.delete()

        return Response({"message": "Cart Item successfully deleted!"}, status=status.HTTP_202_ACCEPTED)
    
    @swagger_auto_schema(operation_description="This is for update cart functionality API",
                         request_body=serializers.UpdateCartSerializer)
    def patch(self, request, *args, **kwargs):
        user = request.user
        cart, _created = models.Cart.objects.get_or_create(
            user=user
        )
        quantity = request.data["quantity"]

        cart_item = get_object_or_404(models.CartItem, id=request.data["cartid"], cart=cart)

        serializer = serializers.CartSerializer(
                data=request.data, 
                context={'request': request, 'quantity': quantity, 
                         'cart_item': cart_item}
            )

        if serializer.is_valid():
            serializer.update(cart_item, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
