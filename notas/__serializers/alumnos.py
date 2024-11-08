from rest_framework import serializers
from ..models import Alumnos, Cursos, Secciones, Grados

class ListCursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = ('id','nombre_curso')

class AlumnosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumnos
        read_only_fields = ('id', 'fecha_creacion_alumno')
        exclude = ('estado_alumno',)

    def validate(self, data):
        nombre_alumno = data.get('nombre_alumno')
        apellido_alumno = data.get('apellido_alumno')

        # Obtener el grado y los cursos seleccionados
        grado_id = data.get('grado_id')
        cursos_seleccionados = data.get('curso_id', [])

        # Obtener los cursos permitidos para el grado seleccionado
        cursos_permitidos = set(Cursos.objects.filter(grado_id=grado_id).values_list('id', flat=True))

        # Convertir cursos_seleccionados a un conjunto de IDs
        cursos_seleccionados_ids = set(curso.id for curso in cursos_seleccionados)

        # Verificar que todos los cursos seleccionados están en los cursos permitidos
        if not cursos_seleccionados_ids.issubset(cursos_permitidos):
            raise serializers.ValidationError({
                "message": "Algunos de los cursos seleccionados no pertenecen al grado especificado."
            })

        # Validación para evitar duplicados de nombre y apellido
        if self.instance:
            if Alumnos.objects.filter(nombre_alumno=nombre_alumno, apellido_alumno=apellido_alumno).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({"message": "Este alumno ya está asignado a un grado"})  
        else:
            if Alumnos.objects.filter(nombre_alumno=nombre_alumno, apellido_alumno=apellido_alumno).exists():
                raise serializers.ValidationError({"message": "Este alumno ya está asignado a un grado"})  

        return data

    def get_all_cursos(self, instance):
        # Filtrar cursos según el grado del alumno
        if instance.grado_id:
            cursos_permitidos = Cursos.objects.filter(grado_id=instance.grado_id, estado_curso=True)
            
            # Personalizar la salida cambiando 'nombre_curso' a 'value'
            return [
                {
                    'id': curso.id,
                    'value': curso.nombre_curso  # Renombrar 'nombre_curso' a 'value'
                }
                for curso in cursos_permitidos
            ]
        return []

    def get_selected_cursos(self, instance):
        """
        Filtrar solo los cursos seleccionados por el usuario que pertenecen al grado del alumno.
        """
        if instance.grado_id:
            cursos_seleccionados = instance.curso_id.filter(grado_id=instance.grado_id)
            
            # Personalizar la salida de cada curso en el formato deseado
            return [
                {
                    'id': curso.id,
                    'value': curso.nombre_curso  # Cambiamos 'nombre_curso' a 'value'
                }
                for curso in cursos_seleccionados
            ]
        return []
    
    def get_grados_options(self):
        # Consultar todos los grados y formatear la salida
        return [
            {
                'id': grado.id,
                'value': grado.nombre_grado
            } for grado in Grados.objects.filter(estado_grado=True)
        ]
    
    def get_secciones_options(self):
        # Obtener solo secciones únicas basadas en el nombre
        unique_secciones = Secciones.objects.filter(estado_seccion=True).values('nombre_seccion').distinct()
        # Mapear a la estructura esperada, usando el primer id disponible para cada nombre
        return [
            {
                'id': Secciones.objects.filter(nombre_seccion=seccion['nombre_seccion']).first().id,
                'value': seccion['nombre_seccion']
            } for seccion in unique_secciones
        ]

    def to_representation(self, instance):
        # Usamos `get_selected_cursos` en lugar de `get_cursos` para que solo se muestren los cursos seleccionados
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
                'value': instance.nombre_alumno,
                'disabled': False,
                'multiple': False
            },
            'Apellido': {
                'tag': 'input',
                'type': 'text',
                'value': instance.apellido_alumno,
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
            },
            'Seccion': {
                'tag': 'select',
                'type': 'text',
                'value': instance.seccion_id.id,
                'disabled': False,
                'multiple': False,
                'options': self.get_secciones_options()
            },
            'Curso': {
                'tag': 'select',
                'type': 'text',
                'value': self.get_selected_cursos(instance),
                'disabled': False,
                'multiple': True,
                'options': self.get_all_cursos(instance),
            }
        }
