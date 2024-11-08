from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import AlumnosSerializer
from .http_states import *
from ..permission import CanPerformAction

class AlumnosViewSet(viewsets.ModelViewSet):
    queryset = AlumnosSerializer.Meta.model.objects.filter(estado_alumno=True)
    serializer_class = AlumnosSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_alumno=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_alumno=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Alumno creado con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            alumno_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if alumno_serializer.is_valid():
                alumno_serializer.save()
                return Response({'status': 'Alumno actualizado con exito', 'data': alumno_serializer.data}, status=estados['ok'])
            return Response(alumno_serializer.errors, status=estados['bad_request'])
        return Response({'status': 'No existe ningun alumno con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        alumno = self.get_queryset().filter(id=pk).first()
        if alumno:
            alumno.estado_alumno = False
            alumno.save()
            return Response({'status': 'Alumno eliminado con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ningun alumno con ese id'}, status=estados['not_found'])