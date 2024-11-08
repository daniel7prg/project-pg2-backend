from rest_framework.permissions import BasePermission
from .models import UserTypes

class HasRolePermission(BasePermission):
    allowed_roles_by_method = {}

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # Obtener los roles permitidos según el método HTTP
        allowed_roles = self.allowed_roles_by_method.get(request.method, [])
        return user.user_type in allowed_roles
    
class CanPerformAction(HasRolePermission):
    allowed_roles_by_method = {
        'GET': [UserTypes.ADMINISTRADOR, UserTypes.SECRETARIO, UserTypes.PROFESOR],
        'POST': [UserTypes.ADMINISTRADOR, UserTypes.SECRETARIO ],
        'PUT': [UserTypes.ADMINISTRADOR, UserTypes.SECRETARIO, UserTypes.PROFESOR],
        'PATCH': [UserTypes.ADMINISTRADOR, UserTypes.SECRETARIO, UserTypes.PROFESOR],
        'DELETE': [UserTypes.ADMINISTRADOR ],
    }