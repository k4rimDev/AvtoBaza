from django.urls import path

from apps.product.api import views
    

urlpatterns = [
    # Base Product URLs
    path('brands', views.BrandsAPIView.as_view(), name='brands'),
    path('groups', views.GroupsAPIView.as_view(), name='groups'),
    path('discounts', views.DiscountsAPIView.as_view(), name='discounts'),
    path('price-complaints', views.PriceComplaintsAPIView.as_view(), name='price_complaints'),
    path('popup-slider', views.PopUpSliderAPIView.as_view(), name='popup_slider'),
    path('discount-info', views.DiscountInfoAPIView.as_view(), name='discount_info'),
    
    # Product filter URLs
    path('filter-products', views.FilterProductsAPIView.as_view(), name='filter_products'),
    path('detail/<str:slug>', views.ProductDetailAPIView.as_view(), name='product_detail'),
]
