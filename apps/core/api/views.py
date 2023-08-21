from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

class SliderAPIView(APIView):
    def get(self, *args, **kwargs):
        return JsonResponse({"msg": "sdf"})