from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..models import UserProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        read_only_fields = ('id',)
        exclude = ('is_staff', 'is_active', 'is_superuser')
    
    def to_representation(self, instance):
        return{
            'id': instance.id,
            'username': instance.username,
            'name': f'{instance.first_name} {instance.last_name}',
            'user_type': instance.user_type
        }