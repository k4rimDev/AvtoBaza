from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.product import models
from apps.product.api import serializers

from apps.core import models as core_models


class FilterProductAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        slider_obj = get_object_or_404(core_models.Slider, slug=slug)
        queryset = slider_obj.products.all().order_by("name")
        serializer = serializers.ProductSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
    
class BrandsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.Brand.objects.all()
        serializer = serializers.BrandSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

class GroupsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.BrandGroup.objects.all()
        serializer = serializers.BrandGroupSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
    
class DiscountsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.Discount.objects.filter(is_active=True)
        serializer = serializers.DiscountSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 

class FilterProductsAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

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

        serializer = serializers.ProductSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK) 
