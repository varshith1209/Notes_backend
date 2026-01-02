from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, MeView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),

    # Login
    path('token/', TokenObtainPairView.as_view()),
    # Refresh Token
    path('token/refresh/', TokenRefreshView.as_view()),
]
        