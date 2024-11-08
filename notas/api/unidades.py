from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import UnidadesSerializer
from .http_states import *
from ..permission import CanPerformAction

class UnidadesViewSet(viewsets.ModelViewSet):
    queryset = UnidadesSerializer.Meta.model.objects.filter(estado_unidad=True)
    serializer_class = UnidadesSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_unidad=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_unidad=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Unidad creada con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            unidad_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if unidad_serializer.is_valid():
                unidad_serializer.save()
                return Response({'status': 'Unidad actualizada con exito', 'data': unidad_serializer.data}, status=estados['ok'])
            return Response(unidad_serializer.errors, status=estados['bad_request'])
        return Response({'status': 'No existe ninguna unidad con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        unidad = self.get_queryset().filter(id=pk).first()
        if unidad:
            unidad.estado_unidad = False
            unidad.save()
            return Response({'status': 'Unidad eliminada con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ninguna unidad con ese id'}, status=estados['not_found'])