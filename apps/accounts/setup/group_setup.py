from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

def create_groups():
    User = get_user_model()
    user_ct = ContentType.objects.get_for_model(User)

    # Create groups
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    owner_group, _ = Group.objects.get_or_create(name='BusinessOwner')
    management_group, _ = Group.objects.get_or_create(name='Manager')
    worker_group, _ = Group.objects.get_or_create(name='Worker')

    # Get user permissions
    all_user_perms = Permission.objects.filter(content_type=user_ct)
    add_change_delete_view = all_user_perms.filter(
        codename__in=['add_user', 'change_user', 'delete_user', 'view_user']
    )
    view_perm = all_user_perms.filter(codename='view_user')

    # Assign permissions
    admin_group.permissions.set(all_user_perms)
    owner_group.permissions.set(add_change_delete_view)
    management_group.permissions.set(add_change_delete_view)
    worker_group.permissions.set(view_perm)

    print("Custom groups and permissions set.")
