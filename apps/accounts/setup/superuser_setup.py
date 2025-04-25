from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

def create_super_admin():
    User = get_user_model()

    username = 'admin'
    email = 'admin@example.com'
    password = 'adminpassword'

    if User.objects.filter(username=username).exists():
        print("Superuser already exists.")
        return

    # Create superuser
    superuser = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    # Assign to Admin group
    try:
        admin_group = Group.objects.get(name='Admin')
    except ObjectDoesNotExist:
        admin_group = Group.objects.create(name='Admin')
        print("Admin group created (no permissions assigned).")

    superuser.groups.add(admin_group)
    print(f"Superuser '{username}' created and added to Admin group.")