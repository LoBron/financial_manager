from django.contrib.auth import authenticate
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from users.models import User
from users.utils import send_email_to_verify


class UserViewSet(DjoserUserViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = get_object_or_404(User, id=serializer.data.get('id'))
        send_email_to_verify(self.request, user, use_https=False)
        return Response(
            {
                'message': f'Пользователь создан. Проверьте свою почту '
                           f'{serializer.data.get("email")} и завершите '
                           f'регистрацию.'
            },
            status=status.HTTP_201_CREATED, headers=headers
        )
