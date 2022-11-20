from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter, DefaultRouter
from .yasg import urlpatterns as doc_urls

from manager.views import *
from users.views import TokenCreateView
from users.viewsets import UserViewSet

user_router = DefaultRouter()
user_router.register("users", UserViewSet)

transaction_router = SimpleRouter()
transaction_router.register(r'transactions', TransactionViewSet)

category_router = SimpleRouter()
category_router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    path('auth/', include(user_router.urls)),
    re_path(r"^auth/token/login/?$", TokenCreateView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('api/v1/', include(transaction_router.urls)),
    path('api/v1/', include(category_router.urls)),
    path('api/v1/manager/', include('manager.urls')),
]

urlpatterns += doc_urls
