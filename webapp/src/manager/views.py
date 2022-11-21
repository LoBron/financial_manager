from decimal import Decimal
from djoser.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .utils import TransactionFilter, check_balance, get_user_statistics
from .serializers import *
from . import tasks


class ProfileAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'user': serializer.data,
            'balance': check_balance(request.user.pk),
        })


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def get_queryset(self):
        return Transaction.objects.filter(
            category__user=self.request.user.pk
        )


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(
            user=self.request.user.pk
        )


class CeleryTaskView(View):
    def get(self, request):
        tasks.some_sleep_task.delay()
        return render(request, 'users/success_verify.html')
