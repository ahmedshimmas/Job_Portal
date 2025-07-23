from rest_framework.permissions import BasePermission
from jobs.models import RolePermission 

class HasRolePermission(BasePermission):
    def has_permission(self, request, view):
        
        #get the model name in lowercase
        model_name = view.queryset.model.__name__.lower()

        #get the action
        action = view.action

        #construct permission code
        required_permission = f'{model_name}_{action}'

        #check if user role has the permission in RolePermission 
        return RolePermission.objects.filter(
            role=request.user.role,
            permission__code = required_permission
        ).exists()

