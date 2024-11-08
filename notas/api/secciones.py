from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import SeccionesSerializer
from .http_states import *
from ..permission import CanPerformAction

class SeccionesViewSet(viewsets.ModelViewSet):
    queryset = SeccionesSerializer.Meta.model.objects.filter(estado_seccion=True)
    serializer_class = SeccionesSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_seccion=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_seccion=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Seccion creada con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            seccion_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if seccion_serializer.is_valid():
                seccion_serializer.save()
                return Response({'status': 'Seccion actualizada con exito', 'data': seccion_serializer.data}, status=estados['ok'])
            return Response(seccion_serializer.errors['nombre_seccion'], status=estados['bad_request'])
        return Response({'status': 'No existe ninguna seccion con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        seccion = self.get_queryset().filter(id=pk).first()
        print(seccion)
        if seccion:
            seccion.estado_seccion = False
            seccion.save()
            return Response({'status': 'Seccion eliminada con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ninguna seccion con ese id'}, status=estados['not_found'])