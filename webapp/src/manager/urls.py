from django.urls import path

from .views import *

urlpatterns = [
    path('profile/', ProfileAPIView.as_view()),
]