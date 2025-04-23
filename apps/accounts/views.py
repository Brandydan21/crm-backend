from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import AdminUserSerializer
from .permissions import IsAdminGroupOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import Group

User = get_user_model()

# -----------------------------
# Admin ViewSet
# -----------------------------

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsAdminGroupOnly]

    def perform_create(self, serializer):
        if not self.request.user.groups.filter(name='Admin').exists():
            raise PermissionDenied("Only Admins can create users.")

        role = self.request.data.get('role', 'worker').capitalize()
        if role not in ['Manager', 'Worker']:
            raise PermissionDenied("Admins can only assign 'Manager' or 'Worker' roles.")

        instance = serializer.save()
        self._assign_group(instance, role)

    def perform_update(self, serializer):
        if not self.request.user.groups.filter(name='Admin').exists():
            raise PermissionDenied("Only Admins can create users.")

        role = self.request.data.get('role')
        if role:
            role = role.capitalize()
            self._check_role_permission(role)
        instance = serializer.save()
        if role:
            self._assign_group(instance, role)

    def perform_destroy(self, instance):
        instance.delete()

    def _assign_group(self, user, role):
        try:
            group = Group.objects.get(name=role)
            user.groups.set([group])
        except Group.DoesNotExist:
            raise PermissionDenied(f"Invalid role: {role}")

    def _check_role_permission(self, role):
        # Admin can assign any role, but we're limiting to Manager and Worker explicitly above.
        pass

