from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.core.api import views


urlpatterns = [
    path('slider/', views.SliderAPIView.as_view(), name='slider'),
    path('campaign-text/', views.CampaignTextAPIView.as_view(), name='campaign_text'),
    path('main-data/', views.MainDataAPIView.as_view(), name='main_data'),
    path('brand-numbers/', views.BrandNumbersAPIView.as_view(), name='brand_numbers'),
    path('about-us/', views.AboutUsAPIView.as_view(), name='about_us'),
    path('suggestions-complaints/', views.SuggestionComplaintAPIView.as_view(), name='suggestions_complaints'),
]
