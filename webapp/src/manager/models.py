from django.db import models

from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(
        'users.User', verbose_name='Пользователь', on_delete=models.CASCADE
    )
    name = models.CharField('Название категории', max_length=256)
    is_income = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        unique_together = ('user', 'name')
        # indexes = [
        #     models.Index(fields=['id', 'user', 'name', 'is_income']),
        # ]

    def __str__(self):
        return self.name

    # def save(
    #         self, force_insert=False, force_update=False,
    #         using=None, update_fields=None
    # ):
    #     if (
    #             update_fields is not None
    #             and "is_income" in update_fields
    #     ):
    #         is_income_changed = True
    #     else:
    #         is_income_changed = False
    #
    #     super().save(
    #         force_insert=force_insert,
    #         force_update=force_update,
    #         using=using,
    #         update_fields=update_fields,
    #     )
    #
    #     if is_income_changed:
    #         recalculation_income_and_expenses(self)


class Transaction(models.Model):
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE
    )
    amount = models.DecimalField('Cумма', max_digits=9, decimal_places=2)
    organization = models.CharField(
        'Организация', max_length=256, blank=True, null=True
    )
    description = models.CharField(
        'Описание', max_length=256, blank=True, null=True
    )
    time_create = models.TimeField('Время', default=timezone.now().time())
    date_create = models.DateField('Дата', default=timezone.now().date())



    # def save(self, *args, **kwargs):
    #     difference = self.amount - self.previous_amount
    #     is_income = Category.objects.get(pk=self.category_id).is_income
    #
    #     if difference != 0:
    #         self.previous_amount = self.amount
    #
    #     super().save(*args, **kwargs)
    #
    #     if difference != 0:
    #         profile = Profile.objects.get(user__category=self.category_id)
    #         if is_income:
    #             profile.income += difference
    #         else:
    #             profile.expenses += difference
    #         profile.save()
    #
    # def delete(self, *args, **kwargs):
    #     amount = self.previous_amount
    #     is_income = Category.objects.get(pk=self.category_id).is_income
    #
    #     delete_result = super().delete(*args, **kwargs)
    #
    #     profile = Profile.objects.get(user__category=self.category_id)
    #     if is_income:
    #         profile.income -= amount
    #     else:
    #         profile.expenses -= amount
    #     profile.save()
    #
    #     return delete_result


# class Profile(models.Model):
#     user = models.OneToOneField(
#         'users.User', verbose_name='Пользователь', on_delete=models.CASCADE
#     )
#     income = models.DecimalField(
#         'Доходы', max_digits=12, decimal_places=2, default=0
#     )
#     expenses = models.DecimalField(
#         'Расходы', max_digits=12, decimal_places=2, default=0
#     )
#     date_time_change = models.DateTimeField(
#         'Дата и время изменения', auto_now=True
#     )
