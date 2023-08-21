from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.core.api import views
    

urlpatterns = [
    # Slider
    path('slider/', views.SliderAPIView.as_view(), name='slider'),
    
]
