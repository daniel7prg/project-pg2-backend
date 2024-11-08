from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class Grados(models.Model):
    nombre_grado = models.CharField(max_length=50, blank=False, null=False)
    estado_grado = models.BooleanField(default=True)
    fecha_creacion_grado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_grado

class Secciones(models.Model):
    nombre_seccion = models.CharField(max_length=10, blank=False, null=False)
    estado_seccion = models.BooleanField(default=True)
    fecha_creacion_seccion = models.DateTimeField(auto_now_add=True)
    grado_id = models.ForeignKey(Grados, on_delete=models.CASCADE, verbose_name="seccion")

    def __str__(self):
        return self.nombre_seccion

class Unidades(models.Model):
    nombre_unidad = models.CharField(max_length=50, blank=False, null=False, unique=True)
    estado_unidad = models.BooleanField(default=True)
    fecha_creacion_unidad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_unidad

class Cursos(models.Model):
    nombre_curso = models.CharField(max_length=50, blank=False, null=False, unique=True)
    estado_curso = models.BooleanField(default=True)
    fecha_creacion_curso = models.DateTimeField(auto_now_add=True)
    grado_id = models.ForeignKey(Grados, on_delete=models.CASCADE, verbose_name="grado")

    def __str__(self):
        return self.nombre_curso

class Alumnos(models.Model):
    nombre_alumno = models.CharField(max_length=50, blank=False, null=False)
    apellido_alumno = models.CharField(max_length=50, blank=False, null=False)
    estado_alumno = models.BooleanField(default=True)
    fecha_creacion_alumno = models.DateTimeField(auto_now_add=True)
    grado_id = models.ForeignKey(Grados, on_delete=models.CASCADE, verbose_name="grado")
    seccion_id = models.ForeignKey(Secciones, on_delete=models.CASCADE, verbose_name="seccion")
    curso_id = models.ManyToManyField(Cursos, verbose_name="curso")

    def __str__(self):
        return self.nombre_alumno

class Notas(models.Model):
    valor_nota = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], null=False, default=0)
    valor_talento = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], null=False, default=0)
    estado_nota = models.BooleanField(default=True)
    fecha_creacion_nota = models.DateTimeField(auto_now_add=True)
    alumno_id = models.ForeignKey(Alumnos, on_delete=models.CASCADE, verbose_name="alumno")
    unidad_id = models.ForeignKey(Unidades, on_delete=models.CASCADE, verbose_name="unidad")
    curso_id = models.ManyToManyField(Cursos, verbose_name="curso")

class UserTypes(models.IntegerChoices):
    ADMINISTRADOR = 1, 'Administrador'
    SECRETARIO = 2, 'Secretario'
    PROFESOR = 3, 'Profesor'

class UserManager(BaseUserManager):
    def _create_user(self, username, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            first_name = first_name,
            last_name = last_name,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        return self._create_user(username, email, first_name, last_name, password, True, True, **extra_fields)

class UserProfile(AbstractUser): 
    username = models.CharField(max_length = 255, unique = True)
    user_type = models.IntegerField(choices=UserTypes.choices, default=UserTypes.PROFESOR)
    first_name = models.CharField(max_length=150, blank=False, null=True)
    last_name = models.CharField(max_length=150, blank=False, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    curso_id = models.ManyToManyField(Cursos, verbose_name='cursos', blank=True)
    grado_id = models.ManyToManyField(Grados, verbose_name='grados', blank=True)
    seccion_id = models.ManyToManyField(Secciones, verbose_name='secciones', blank=True)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_type','first_name','last_name','email']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'