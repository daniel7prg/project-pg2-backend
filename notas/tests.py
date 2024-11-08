from django.test import TestCase

# Create your tests here.
from notas.models import UserProfile

user = UserProfile.objects.get(username='dani77')  # Reemplaza con el username correcto
print (user.username)
user.is_active = True
print (user.is_active)
#user.set_password('daniel2002sanzz')
user.save()