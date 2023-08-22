from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.product.api import views
    

urlpatterns = [
    path('brands', views.BrandsAPIView.as_view(), name='brands'),
    path('groups', views.GroupsAPIView.as_view(), name='groups'),
    path('discounts', views.DiscountsAPIView.as_view(), name='discounts'),
    
    # Product filter
    path('filter-product/<str:slug>', views.FilterProductAPIView.as_view(), name='filter_product'),
    path('filter-products', views.FilterProductsAPIView.as_view(), name='filter_products'),
]
