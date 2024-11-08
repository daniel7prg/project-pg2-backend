from rest_framework import serializers
from ..models import Cursos, Grados

class CursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        read_only_fields = ('id','fecha_creacion_curso')
        exclude = ('estado_curso',)

    def get_grados_options(self):
        # Consultar todos los grados y formatear la salida
        return [
            {
                'id': grado.id,
                'value': grado.nombre_grado
            } for grado in Grados.objects.all()
        ]

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
                'value': instance.nombre_curso,
                'disabled': False,
                'multiple': False
            },
            'Grado': {
                'tag': 'select',
                'type': 'text',
                'value': instance.grado_id.id,
                'disabled': False,
                'multiple': False,
                'options': self.get_grados_options()
            }
        }