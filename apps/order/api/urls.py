from django.urls import path

from apps.order.api import views
    

urlpatterns = [
    # Cart APIs
    path('cart/', views.CartAPIView.as_view(), name='cart'),

    # Order APIs
    path('orders/', views.OrderAPIView.as_view(), name='order'),
    path('orders/<str:transaction_id>', views.OrderDetailAPIView.as_view(), name='order_detail'),
]
