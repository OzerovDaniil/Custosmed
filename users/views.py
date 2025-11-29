from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserProfileSerializer


class RegisterView(generics.CreateAPIView):
    """
    View для регистрации нового пользователя.
    Доступ разрешен всем (AllowAny).
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    """
    View для получения профиля текущего авторизованного пользователя.
    Доступ только для авторизованных пользователей (IsAuthenticated).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
