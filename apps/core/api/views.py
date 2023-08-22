from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse

from apps.core import models
from apps.core.api import serializers


class SliderAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.Slider.objects.filter(is_active=True).order_by("order_count")
        serializer = serializers.SliderSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CampaignTextAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.CampaignText.objects.filter(is_active=True)
        serializer = serializers.CampaignTextSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MainDataAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.MainData.objects.first()
        serializer = serializers.MainDataSerializer(queryset, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)

class BrandNumbersAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.BrandNumber.objects.all()
        serializer = serializers.BrandNumberSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
