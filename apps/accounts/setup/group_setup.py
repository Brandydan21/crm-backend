from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

def create_groups():
    User = get_user_model()
    user_ct = ContentType.objects.get_for_model(User)

    # Create or get groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    worker_group, _ = Group.objects.get_or_create(name='Worker')

    # Permissions
    perms = Permission.objects.filter(content_type=user_ct)

    # Assign all user perms to Admin
    admin_group.permissions.set(perms)

    # Assign limited perms to Manager
    manager_perms = perms.filter(codename__in=[
        'add_user', 'change_user', 'delete_user', 'view_user'
    ])
    manager_group.permissions.set(manager_perms)

    # Workers get only view permission
    worker_perms = perms.filter(codename='view_user')
    worker_group.permissions.set(worker_perms)

    print("Groups and permissions set.")
