from rest_framework import serializers
from ..models import UserProfile, Grados, Cursos, Secciones

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        read_only_fields = ('id',)
        exclude = ('is_staff', 'is_active', 'is_superuser')

    def create(self, validated_data):
        # Extraemos los datos Many-to-Many de 'curso_id' y 'grado_id'
        cursos_data = validated_data.pop('curso_id', [])
        grados_data = validated_data.pop('grado_id', [])
        
        # Creamos el usuario sin los campos Many-to-Many
        user = UserProfile(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        
        # Asignamos las relaciones Many-to-Many después de guardar el usuario
        if cursos_data:
            user.curso_id.set(cursos_data)
        if grados_data:
            user.grado_id.set(grados_data)
        
        return user
    
    def get_all_cursos(self):
        """
        Filtrar cursos según los grados asociados al usuario.
        """
        cursos_permitidos = []
        for grado in Grados.objects.all():  # Iteramos sobre cada grado en grado_id
            cursos_permitidos.extend(Cursos.objects.filter(grado_id=grado, estado_curso=True))
        
        # Eliminamos duplicados si un curso se repite en múltiples grados
        cursos_permitidos = list({curso.id: curso for curso in cursos_permitidos}.values())

        # Personalizamos la salida cambiando 'nombre_curso' a 'value'
        return [
            {
                'id': curso.id,
                'value': curso.nombre_curso
            }
            for curso in cursos_permitidos
        ]

    def get_selected_cursos(self, instance):
        """
        Filtrar solo los cursos seleccionados por el usuario que pertenecen a los grados asociados.
        """
        cursos_seleccionados = []
        for grado in instance.grado_id.all():
            cursos_seleccionados.extend(instance.curso_id.filter(grado_id=grado))

        # Eliminamos duplicados en caso de repetidos
        cursos_seleccionados = list({curso.id: curso for curso in cursos_seleccionados}.values())

        # Personalizamos la salida en el formato deseado
        return [
            {
                'id': curso.id,
                'value': curso.nombre_curso
            }
            for curso in cursos_seleccionados
        ]

    def get_all_grados(self):
        grados_seleccionados = Grados.objects.filter(estado_grado=True)
        
        # Personalizar la salida cambiando 'nombre_curso' a 'value'
        return [
            {
                'id': grado.id,
                'value': grado.nombre_grado  # Renombrar 'nombre_curso' a 'value'
            }
            for grado in grados_seleccionados
        ]

    def get_selected_grados(self, instance):
        grados_permitidos = instance.grado_id.all()
        
        # Personalizar la salida cambiando 'nombre_curso' a 'value'
        return [
            {
                'id': grado.id,
                'value': grado.nombre_grado  # Renombrar 'nombre_curso' a 'value'
            }
            for grado in grados_permitidos
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
    
    def get_selected_secciones(self, instance):
        secciones_permitidos = instance.seccion_id.all()
        
        # Personalizar la salida cambiando 'nombre_curso' a 'value'
        return [
            {
                'id': seccion.id,
                'value': seccion.nombre_seccion  # Renombrar 'nombre_curso' a 'value'
            }
            for seccion in secciones_permitidos
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
            'Nombre_Usuario': {
                'tag': 'input',
                'type': 'text',
                'value': instance.username,
                'disabled': False,
                'multiple': False
            },
            'Nombre': {
                'tag': 'input',
                'type': 'text',
                'value': instance.first_name,
                'disabled': False,
                'multiple': False
            },
            'Apellido': {
                'tag': 'input',
                'type': 'text',
                'value': instance.last_name,
                'disabled': False,
                'multiple': False
            },
            'Rol': {
                'tag': 'select',
                'type': 'text',
                'value': instance.user_type,
                'disabled': False,
                'multiple': False,
                'options': [
                    {'id': 1, 'value': 'Administrador'},
                    {'id': 2, 'value': 'Secretario'},
                    {'id': 3, 'value': 'Profesor'},
                ]
            },
            'Grados': {
                'tag': 'select',
                'type': 'text',
                'value': self.get_selected_grados(instance),
                'disabled': False,
                'multiple': True,
                'options': self.get_all_grados(),
            },
            'Secciones': {
                'tag': 'select',
                'type': 'text',
                'value': self.get_selected_secciones(instance),
                'disabled': False,
                'multiple': True,
                'options': self.get_secciones_options()
            },
            'Cursos': {
                'tag': 'select',
                'type': 'text',
                'value': self.get_selected_cursos(instance),
                'disabled': False,
                'multiple': True,
                'options': self.get_all_cursos(),
            },
            'Password': {
                'tag': 'input',
                'type': 'password',
                'value': instance.password,
                'disabled': True,
                'multiple': False
            },
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        read_only_fields = ('id',)
        exclude = ('is_staff', 'is_active', 'is_superuser', 'password')

class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=128, min_length=8, write_only=True)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({'status':'Las contraseñas no coinciden'}) 
        return data