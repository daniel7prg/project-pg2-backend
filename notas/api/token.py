from rest_framework_simplejwt.views import TokenObtainPairView
from ..__serializers.token import CustomTokenObtainPairSerializer, CustomUserSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .http_states import *

class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de sesión exitoso',
                    'logged': True
                }, status=estados['ok'])
            return Response(login_serializer.errors, status=estados['bad_request'])
        return Response({'message': 'Usuario o contraseña incorrectos'}, status=estados['bad_request'])
    