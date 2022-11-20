from decimal import Decimal
from djoser.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .utils import TransactionFilter
from .serializers import *


class ProfileAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)

        income = Decimal('0')
        expenses = Decimal('0')
        transactions = Transaction.objects.filter(
            category__user=request.user.pk
        ).select_related('category')
        for transaction in transactions:
            if transaction.category.is_income:
                income += transaction.amount
            else:
                expenses += transaction.amount

        return Response({
            'user': serializer.data,
            'balance': {
                'income': income,
                'expenses': expenses,
            }
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
