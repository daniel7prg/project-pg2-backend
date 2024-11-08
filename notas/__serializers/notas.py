from rest_framework import serializers
from ..models import Notas, Unidades, Cursos, Grados, Secciones, Alumnos

class NotasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notas
        read_only_fields = ('id','fecha_creacion_nota')
        exclude = ('estado_nota',)

    def validate(self, data):
        alumno = data.get('alumno_id')
        unidad = data.get('unidad_id')
        cursos_seleccionados = data.get('curso_id', [])

        # Excluir la instancia actual en caso de actualización
        nota_id = self.instance.id if self.instance else None
        
        # Validar si ya existe una nota para el alumno en la misma unidad y cursos seleccionados
        if Notas.objects.filter(alumno_id=alumno, unidad_id=unidad, curso_id__in=cursos_seleccionados).exclude(id=nota_id).exists():
            raise serializers.ValidationError({
                "message": "Este alumno ya tiene una nota asignada para uno o más de los cursos seleccionados en esta unidad."
            })

        # Validar que todos los cursos seleccionados pertenecen al grado del alumno
        for curso in cursos_seleccionados:
            if not Cursos.objects.filter(id=curso.id, grado_id=alumno.grado_id.id, estado_curso=True).exists():
                raise serializers.ValidationError({
                    "message": "El curso no pertenece al grado del alumno"
                })

        return data
    
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

    def get_unidades_options(self):
        # Consultar todos los grados y formatear la salida
        return [
            {
                'id': unidad.id,
                'value': unidad.nombre_unidad
            } for unidad in Unidades.objects.filter(estado_unidad=True)
        ]
    
    def get_alumnos_options(self):
        # Consultar todos los grados y formatear la salida
        return [
            {
                'id': alumnos.id,
                'value': f'{alumnos.nombre_alumno} {alumnos.apellido_alumno}'
            } for alumnos in Alumnos.objects.filter(estado_alumno=True)
        ]
    
    def get_cursos_options(self, instance):
        """
        Filtrar solo los cursos seleccionados por el usuario que pertenecen al grado del alumno.
        """
        if instance.alumno_id.grado_id:
            cursos_seleccionados = instance.curso_id.filter(grado_id=instance.alumno_id.grado_id)
            
            # Personalizar la salida de cada curso en el formato deseado
            return [
                {
                    'id': curso.id,
                    'value': curso.nombre_curso  # Cambiamos 'nombre_curso' a 'value'
                }
                for curso in cursos_seleccionados
            ]
        return []
    
    def get_cursos_options_all(self, instance):
        # Filtrar cursos según el grado del alumno
        if instance.alumno_id.grado_id:
            cursos_permitidos = Cursos.objects.filter(grado_id=instance.alumno_id.grado_id, estado_curso=True)
            
            # Personalizar la salida cambiando 'nombre_curso' a 'value'
            return [
                {
                    'id': curso.id,
                    'value': curso.nombre_curso  # Renombrar 'nombre_curso' a 'value'
                }
                for curso in cursos_permitidos
            ]
        return []

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
                'tag': 'select',
                'type': 'text',
                'value': instance.alumno_id.id,
                'disabled': True,
                'multiple': False,
                'options': self.get_alumnos_options()
            },
            'Grado': {
                'tag': 'select',
                'type': 'text',
                'value': instance.alumno_id.grado_id.id,
                'disabled': True,
                'multiple': False,
                'options': self.get_grados_options()
            },
            'Seccion': {
                'tag': 'select',
                'type': 'text',
                'value': instance.alumno_id.seccion_id.id,
                'disabled': True,
                'multiple': False,
                'options': self.get_secciones_options()
            },
            'Curso': {
                'tag': 'select',
                'type': 'text',
                'value': self.get_cursos_options(instance),
                'disabled': False,
                'multiple': True,
                'options': self.get_cursos_options_all(instance)
            },
            'Unidad': {
                'tag': 'select',
                'type': 'text',
                'value': instance.unidad_id.id,
                'disabled': False,
                'multiple': False,
                'options': self.get_unidades_options()
            },
            'Nota': {
                'tag': 'input',
                'type': 'number',
                'value': instance.valor_nota,
                'disabled': False,
                'multiple': False
            },
            'Talentos': {
                'tag': 'input',
                'type': 'number',
                'value': instance.valor_talento,
                'disabled': False,
                'multiple': False
            },
        }