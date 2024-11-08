from rest_framework import serializers
from ..models import Unidades

class UnidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidades
        read_only_fields = ('id','fecha_creacion_unidad')
        exclude = ('estado_unidad',)

    def to_representation(self, instance):
        return{
            'ID': {
                'tag': 'input',
                'type': 'number',
                'value': instance.id,
                'disabled': True,
                'multiple': False
            },
            'Nombre':{
                'tag': 'input',
                'type': 'text',
                'value': instance.nombre_unidad,
                'disabled': False,
                'multiple': False
            },
        }