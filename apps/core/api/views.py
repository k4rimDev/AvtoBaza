from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse

from apps.core import models
from apps.core.api import serializers


class SliderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ] 
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.Slider.objects.filter(is_active=True).order_by("order_count")
        serializer = serializers.SliderSerializer(queryset, many=True,
                                                  context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class CampaignTextAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ] 
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.CampaignText.objects.filter(is_active=True)
        serializer = serializers.CampaignTextSerializer(queryset, many=True,
                                                        context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MainDataAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.MainData.objects.first()
        serializer = serializers.MainDataSerializer(queryset, many=False, 
                                                    context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class BrandNumbersAPIView(APIView):
    allowed_methods = ["GET", "HEAD", "OPTIONS"]
    pagination_class=None

    def get(self, request, *args, **kwargs):
        queryset = models.BrandNumber.objects.all()
        serializer = serializers.BrandNumberSerializer(queryset, many=True,
                                                       context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

class SuggestionComplaintAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, ] 
    allowed_methods = ["GET", "HEAD", "OPTIONS", "POST"]
    pagination_class=None

    def post(self, request, *args, **kwargs):
        serializer = serializers.SuggestionComplaintsSerializer(
                data=request.data, 
                context={'request': request}
            )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
