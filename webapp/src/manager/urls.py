from django.urls import path, re_path, include
from djoser.urls.base import router

from .views import *

urlpatterns = [
    path('profile/', ProfileAPIView.as_view()),
    path(
        'celery_test_task/',
        CeleryTaskView.as_view(),
        name='celery_test_task'
    ),
]