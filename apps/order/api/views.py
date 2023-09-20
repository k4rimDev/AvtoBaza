from datetime import datetime

from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.account import models as am

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

class OrderAPIView(APIView):
    allowed_methods = ["GET", "POST", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
            operation_id='Filter orders',
            operation_description='Filter orders by status, created_at',
            manual_parameters=[
                openapi.Parameter('status', openapi.IN_QUERY, type=openapi.TYPE_STRING, 
                                  enum=['all', 'pending', 'done', 'send', 'partially send', 'canceled', 'returned'],
                                  description='Status of orders'),
                openapi.Parameter('from', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE, description='From date to filter as YYYY-MM-DD'),
                openapi.Parameter('to', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE, description='To date to filter as YYYY-MM-DD'),
            ]
        )
    def get(self, request, *args, **kwargs):
        queryset = models.Order.objects.filter(
            user=request.user,
        )
        order_status = request.GET.get("status", None)
        from_date = request.GET.get("from", None)
        to_date = request.GET.get("to", None)

        if order_status:
            queryset = queryset.filter(
                status=order_status
            )
        if from_date:
            queryset = queryset.filter(
                created_at__date__gte=datetime.strptime(from_date, "%Y-%m-%d")
            )

        if to_date:
            queryset = queryset.filter(
                created_at__date__lte=datetime.strptime(to_date, "%Y-%m-%d")
            )

        serializer = serializers.OrderSerializer(
            queryset, many=True, context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="This is for create order functionality API",
                         request_body=serializers.OrderSerializer)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = serializers.OrderSerializer(
                data=request.data, 
                context={'request': request, 'user': user}
            )
        if serializer.is_valid():
            order_instance = serializer.save()
            order_item_serializer = serializers.OrderItemCreateSerializer(
                data=request.data,
                context={'request': request, 'order': order_instance}
            )
            if order_item_serializer.is_valid():
                order_item_serializer.create(order_item_serializer.validated_data)
            else:
                order_instance.delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        transaction_id = self.kwargs.get("transaction_id")
        order_item = get_object_or_404(models.Order, 
                                       transaction_id=transaction_id)
        
        if order_item.user != user:
            return Response({"message": "User can not see this order"}, 
                            status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = serializers.OrderDetailSerializer(order_item, many=False,
                                                       context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class CheckBalanceAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        ids = request.GET.get("ids", None)
        balance = 0
        if ids:
            try:
                for i in ids[1:len(ids) - 1].split(","):
                    try:
                        balance += models.CartItem.objects.get(id=int(i)).total_price
                    except:    
                        balance += 0

                user_balance = am.Balance.objects.get(user=user).balance

                if balance < user_balance:
                    return Response({"message": "Balance is enough!"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Balance is not enough!"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"message": "Unstuructured list or Unknown cart ID"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Ids is not found!"}, status=status.HTTP_400_BAD_REQUEST)
