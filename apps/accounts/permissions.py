from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name__in=['Admin', 'Manager']).exists()
        )
    
class IsAdminGroupOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()