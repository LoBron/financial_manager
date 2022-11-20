from django.contrib.auth.models import AbstractUser
from django.db import models

from .utils import create_default_categories


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        help_text='Required. 150 characters or fewer. '
                  'Letters, digits and @/./+/-/_ only.',
        validators=[AbstractUser.username_validator],
    )
    email = models.EmailField('email', unique=True)
    email_verify = models.BooleanField('email confirmed', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        indexes = [
            models.Index(fields=['id', 'username', 'email', 'email_verify']),
        ]

    def save(
            self, force_insert=False, force_update=False,
            using=None, update_fields=None
    ):
        if (
                update_fields is not None
                and "email_verify" in update_fields
                and self.email_verify
        ):
            email_verify_changed = True
        else:
            email_verify_changed = False

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

        if email_verify_changed:
            create_default_categories(user=self)
