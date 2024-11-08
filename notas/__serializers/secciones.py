from rest_framework import serializers
from ..models import Secciones, Grados

class SeccionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Secciones
        read_only_fields = ('id', 'fecha_creacion_seccion')
        exclude = ('estado_seccion',)

    def validate(self, data):
        nombre_seccion = data.get('nombre_seccion')
        grado_id = data.get('grado_id')

        if Secciones.objects.filter(nombre_seccion=nombre_seccion, grado_id=grado_id).exists():
            raise serializers.ValidationError({"message": "El grado con esa sección ya existe"})  

        return data

    def get_grados_options(self):
        # Consultar todos los grados y formatear la salida
        return [
            {
                'id': grado.id,
                'value': grado.nombre_grado
            } for grado in Grados.objects.all()
        ]

    def to_representation(self, instance):
        return {
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
                'value': instance.nombre_seccion,
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
