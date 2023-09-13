from django.urls import path

from apps.order.api import views
    

urlpatterns = [
    # Cart
    path('cart/', views.CartAPIView.as_view(), name='cart'),
]
