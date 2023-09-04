from django.urls import path

from apps.account.api import views


urlpatterns = [
    # Account API
    path('auth/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_view'),
    path('auth/token/remove', views.CustomLogoutAPIView.as_view(), name='custom_logout'),
    path('auth/token/refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh_view'),
    path('logout/blacklist/', views.BlacklistTokenUpdateView.as_view(), name='blacklist'),
]
