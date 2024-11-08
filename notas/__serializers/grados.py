from rest_framework import serializers
from ..models import Grados

class GradosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grados
        read_only_fields = ('id','fecha_creacion_grado')
        exclude = ('estado_grado',)

    def to_representation(self, instance):
        return{
            'ID': {
                'tag': 'input',
                'type': 'number',
                'value': instance.id,
                'disabled': True,
                'multiple': False
            },
            'Nombre': {
                'tag': 'input',
                'type': 'text',
                'value': instance.nombre_grado,
                'disabled': False,
                'multiple': False
            }
        }