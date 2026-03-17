from django.urls import path
from .views import RegisterAPIView, ConfirmAPIView, LoginAPIView, CUstomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.google_oauth import GoogleLoginAPIView
urlpatterns = [
    path('users/register/', RegisterAPIView.as_view()),
    path('users/confirm/', ConfirmAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
    
    path('users/api/token/', CUstomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
      path("google-login/", GoogleLoginAPIView.as_view())
]