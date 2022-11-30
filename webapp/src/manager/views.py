from djoser.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import check_balance


class ProfileAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'user': serializer.data,
            'balance': check_balance(request.user.pk),
        })

# class CeleryTaskView(View):
#     def get(self, request):
#         tasks.some_sleep_task.delay()
#         return render(request, 'users/success_verify.html')
