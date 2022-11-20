from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EmailVerify
from .viewsets import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = [
    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(),
        name='verify_email'
    ),
    path('', include('django.contrib.auth.urls')),
]