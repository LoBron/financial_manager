from typing import Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.views import View
from djoser.conf import settings
from djoser.utils import login_user
from djoser.views import TokenCreateView as DjoserTokenCreateView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator \
    as token_generator

from .models import *
from .utils import send_email_to_verify

UserModel = get_user_model()


class TokenCreateView(DjoserTokenCreateView):

    def _action(self, serializer):
        user: User = serializer.user
        if user.email_verify:
            token = login_user(self.request, user)
            token_serializer_class = settings.SERIALIZERS.token
            return Response(
                data=token_serializer_class(token).data,
                status=status.HTTP_200_OK
            )
        else:
            send_email_to_verify(self.request, user, use_https=False)
            return Response(
                data={'error': f'Проверьте свою почту '
                               f'{user.email} и завершите регистрацию.'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class EmailVerify(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user and token_generator.check_token(user, token):
            user.email_verify = True
            user.save(update_fields=['email_verify'])
            return render(request, 'users/success_verify.html')
        else:
            render(request, 'users/invalid_verify.html')

    @staticmethod
    def get_user(uidb64) -> Optional[User]:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
                TypeError, ValueError, OverflowError,
                UserModel.DoesNotExist, ValidationError
        ):
            user = None
        return user
