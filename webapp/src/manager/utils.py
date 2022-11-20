from decimal import Decimal

from django_filters import rest_framework as filters
from .models import *


class TransactionFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name')
    amount = filters.RangeFilter()
    date_create = filters.DateFromToRangeFilter()
    time_create = filters.TimeRangeFilter()
    order_by = filters.OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('amount', 'amount'),
            ('date_create', 'date_create'),
            ('time_create', 'time_create'),
        ),

        # labels do not need to retain order
        # field_labels={
        #     'username': 'User account',
        # }
    )

    class Meta:
        model = Transaction
        fields = ['amount', 'date_create', 'time_create']


def recalculation_income_and_expenses(category) -> None:
    profile = Profile.objects.get(user__category=category.pk)
    transactions = Transaction.objects.filter(
        user=category.user,
        category=category.pk
    )
    amount = Decimal(0)
    if category.is_income:
        for trans in transactions.objects.filter(is_income=False):
            amount += trans.amount
        profile.expenses -= amount
        profile.income += amount
        profile.save()
    else:
        for trans in transactions.objects.filter(is_income=True):
            amount += trans.amount
        profile.expenses += amount
        profile.income -= amount
        profile.save()