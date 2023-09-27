from django.urls import path

from apps.order.api import views
    

urlpatterns = [
    # Cart APIs
    path('cart/', views.CartAPIView.as_view(), name='cart'),

    # Order APIs
    path('orders/', views.OrderAPIView.as_view(), name='order'),
    path('orders/<str:transaction_id>', views.OrderDetailAPIView.as_view(), name='order_detail'),

    # Balance
    path('check-balance/', views.CheckBalanceAPIView.as_view(), name='check_balance'), # Deprecated
    
    # User Account Info
    path('user-account-info/', views.UserAccountInfoAPIView.as_view(), name='user_account_info'),
]
