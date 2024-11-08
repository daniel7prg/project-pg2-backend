from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import UserSerializer, UpdateUserSerializer, PasswordSerializer
from .http_states import *
from ..permission import CanPerformAction

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    update_serializer_class = UpdateUserSerializer
    password_serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(is_active=True)
        return self.get_serializer_class().Meta.model.objects.filter(is_active=True).first()
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Usuario creado con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        user = self.get_queryset().filter(id=pk).first()
        user_serializer = self.update_serializer_class(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'status': 'Usuario actualizado con exito', 'data': user_serializer.data}, status=estados['ok'])
        return Response(user_serializer.errors, status=estados['bad_request'])
    
    def destroy(self, request, pk=None):
        user = self.get_queryset().filter(id=pk).first()
        if user:
            user.is_active = False
            user.save()
            return Response({'status': 'Usuario eliminado con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ningun usuario con ese id'}, status=estados['not_found'])
    
    # Modificar contraseña
    @action(detail=True, methods=['POST'], url_path='cpasswd')
    def change_password(self, request, pk=None):
        user = self.get_queryset().filter(id=pk).first()
        user_serializer = self.password_serializer_class(data=request.data)
        
        if user_serializer.is_valid():
            user.set_password(user_serializer.data['password'])
            user.save()
            return Response({'status': 'Contraseña modificada con exito'}, status=estados['ok'])
        return Response(user_serializer.errors, status=estados['bad_request'])