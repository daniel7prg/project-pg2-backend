from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import CursosSerializer
from .http_states import *
from ..permission import CanPerformAction

class CursosViewSet(viewsets.ModelViewSet):
    queryset = CursosSerializer.Meta.model.objects.filter(estado_curso=True)
    serializer_class = CursosSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_curso=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_curso=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Curso creado con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            curso_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if curso_serializer.is_valid():
                curso_serializer.save()
                return Response({'status': 'Curso actualizado con exito', 'data': curso_serializer.data}, status=estados['ok'])
            return Response(curso_serializer.errors, status=estados['bad_request'])
        return Response({'status': 'No existe ningun curso con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        curso = self.get_queryset().filter(id=pk).first()
        if curso:
            curso.estado_curso = False
            curso.save()
            return Response({'status': 'Curso eliminado con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ningun curso con ese id'}, status=estados['not_found'])