from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import GradosSerializer
from .http_states import *
from ..permission import CanPerformAction

class GradosViewSet(viewsets.ModelViewSet):
    queryset = GradosSerializer.Meta.model.objects.filter(estado_grado=True)
    serializer_class = GradosSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_grado=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_grado=True).first()

    def create(self, request):
        """ grado_ver = self.get_serializer_class().Meta.model.objects.filter(nombre_grado=request.data['nombre_grado']).first()
        seccion_ver = self.get_serializer_class().Meta.model.objects.filter(seccion_id=request.data['seccion_id']).first()

        if grado_ver is None or seccion_ver is None:
            serializer = self.serializer_class(data=request.data)
        else:
            return Response({'status': 'El grado ya existe'}, status=estados['bad_request']) """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Grado creado con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            grado_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if grado_serializer.is_valid():
                grado_serializer.save()
                return Response({'status': 'Grado actualizado con exito', 'data': grado_serializer.data}, status=estados['ok'])
            return Response(grado_serializer.errors, status=estados['bad_request'])
        return Response({'status': 'No existe ningun grado con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        grado = self.get_queryset().filter(id=pk).first()
        if grado:
            grado.estado_grado = False
            grado.save()
            return Response({'status': 'Grado eliminada con exito'}, status=estados['ok'])
        return Response({'status': 'No existe ningun grado con ese id'}, status=estados['not_found']) 