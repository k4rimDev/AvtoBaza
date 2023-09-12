from django.urls import path

from apps.product.api import views
    

urlpatterns = [
    path('brands', views.BrandsAPIView.as_view(), name='brands'),
    path('groups', views.GroupsAPIView.as_view(), name='groups'),
    path('discounts', views.DiscountsAPIView.as_view(), name='discounts'),
    
    # Product filter
    path('filter-products', views.FilterProductsAPIView.as_view(), name='filter_products'),
    path('detail/<str:slug>', views.ProductDetailAPIView.as_view(), name='product_detail'),
]
