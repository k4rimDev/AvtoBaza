from django.shortcuts import get_object_or_404

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.product import models
from apps.product.api import serializers

from apps.utils.mixins import CustomPaginationMixin
from apps.utils.paginations import StandardResultsSetPagination
from apps.utils.permissions import CustomPermissionOnlyGetProducts

    
class BrandsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.Brand.objects.all()
        serializer = serializers.BrandSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

class GroupsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.BrandGroup.objects.all()
        serializer = serializers.BrandGroupSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
    
class DiscountsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.Discount.objects.filter(is_active=True)
        serializer = serializers.DiscountSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

class FilterProductsAPIView(APIView, CustomPaginationMixin):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.Product.objects.all()

        product_code = self.request.GET.get("code")
        brand = self.request.GET.get("brand")
        group = self.request.GET.get("group")
        discount = self.request.GET.get("discount")

        if product_code and product_code is not None:
            queryset = queryset.filter(code = product_code)

        if brand and brand is not None:
            brand = get_object_or_404(models.Brand, slug=brand)
            queryset = queryset.filter(brand=brand)

        if group and group is not None:
            group = get_object_or_404(models.BrandGroup, slug=group)
            queryset = queryset.filter(group=group)

        if discount and discount is not None:
            discount = get_object_or_404(models.Discount, slug=discount)
            queryset = queryset.filter(discount=discount)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializers.ProductSerializer(page, many=True, context={'request': self.request})
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ProductSerializer(page, many=True, context={'request': self.request})

        return Response(serializer.data, status=status.HTTP_200_OK) 

class ProductDetailAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]
    
    def get(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        queryset = get_object_or_404(models.Product, slug=slug)

        serializer = serializers.ProductSerializer(queryset, many=False, 
                                                   context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class PriceComplaintsAPIView(APIView):
    allowed_methods = ["HEAD", "POST", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_description="This is for complaints of user about price of product",
                         request_body=serializers.PriceComplaintsSerializer)
    def post(self, request, *args, **kwargs):
        serializer = serializers.PriceComplaintsSerializer(
                data=request.data, 
                context={'request': request}
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PopUpSliderAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.PopUpSlider.objects.filter(is_active=True).order_by("order_count")
        serializer = serializers.PopUpSliderSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK) 

class DiscountInfoAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None
    permission_classes = [permissions.IsAuthenticated | CustomPermissionOnlyGetProducts]

    def get(self, request, *args, **kwargs):
        queryset = models.DiscountInfo.objects.first()
        serializer = serializers.DiscountInfoSerializer(queryset, many=False, 
                                                        context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK) 
