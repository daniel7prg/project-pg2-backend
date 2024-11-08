from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import NotasSerializer
from .http_states import *
from ..permission import CanPerformAction

class NotasViewSet(viewsets.ModelViewSet):
    queryset = NotasSerializer.Meta.model.objects.filter(estado_nota=True)
    serializer_class = NotasSerializer
    permission_classes = [IsAuthenticated, CanPerformAction]

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer_class().Meta.model.objects.filter(estado_nota=True)
        return self.get_serializer_class().Meta.model.objects.filter(estado_nota=True).first()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Nota creada con exito'}, status=estados['created'])
        return Response(serializer.errors, status=estados['bad_request'])
    
    def partial_update(self, request, pk=None):
        if self.get_queryset(pk):
            nota_serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if nota_serializer.is_valid():
                nota_serializer.save()
                return Response({'status': 'Nota actualizada con exito', 'data': nota_serializer.data}, status=estados['ok'])
            return Response(nota_serializer.errors, status=estados['bad_request'])
        return Response({'status': 'No existe ninguna nota con ese id'}, status=estados['not_found'])
    
    def destroy(self, request, pk=None):
        nota = self.get_queryset().filter(id=pk).first()
        if nota:
            nota.estado_nota = False
            nota.save()
            return Response({'status': 'Nota eliminada con exito'}, status=estados['ok'])    
        return Response({'status': 'No existe ninguna nota con ese id'}, status=estados['not_found'])