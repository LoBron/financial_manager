from decimal import Decimal
from typing import Any

from django_filters import rest_framework as filters
from .models import *


class TransactionFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name')
    amount = filters.RangeFilter()
    date_create = filters.DateFromToRangeFilter()
    time_create = filters.TimeRangeFilter()
    order_by = filters.OrderingFilter(
        fields=(
            ('amount', 'amount'),
            ('date_create', 'date_create'),
            ('time_create', 'time_create'),
        ),
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'date_create', 'time_create']


def check_balance(user_pk: int) -> dict[str, Decimal]:
    income = Decimal('0')
    expenses = Decimal('0')
    transactions = Transaction.objects.filter(
        category__user=user_pk
    ).select_related('category')
    for transaction in transactions:
        if transaction.category.is_income:
            income += transaction.amount
        else:
            expenses += transaction.amount
    return {
        'income': income,
        'expenses': expenses,
    }


def get_user_statistics(user_pk: int) -> list[dict[str, Any]]:
    queryset = (Transaction.objects.
                filter(category__user=user_pk).
                select_related('category').
                values('category__name', 'amount', 'date_create', 'time_create').
                order_by('category__name', 'date_create', 'time_create', 'amount')
                )
    data = {}
    for query in queryset:
        category_name = query.pop('category__name')
        if category_name in data:
            data[category_name].append(query)
        else:
            data[category_name] = [query]
    statistics = []
    for category_name, transactions in data.items():
        statistics.append({'name': category_name, 'transactions': transactions})

    return statistics

# def recalculation_income_and_expenses(category) -> None:
#     profile = Profile.objects.get(user__category=category.pk)
#     transactions = Transaction.objects.filter(
#         user=category.user,
#         category=category.pk
#     )
#     amount = Decimal(0)
#     if category.is_income:
#         for trans in transactions.objects.filter(is_income=False):
#             amount += trans.amount
#         profile.expenses -= amount
#         profile.income += amount
#         profile.save()
#     else:
#         for trans in transactions.objects.filter(is_income=True):
#             amount += trans.amount
#         profile.expenses += amount
#         profile.income -= amount
#         profile.save()
