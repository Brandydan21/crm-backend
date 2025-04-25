def create_owner():
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group
    from apps.accounts.models import Company
    from django.core.exceptions import ValidationError

    User = get_user_model()

    # Step 1: Validate uniqueness of company details
    if Company.objects.filter(business_number='123456789').exists():
        raise ValidationError("A company with this business number already exists.")
    
    if Company.objects.filter(contact_email='admin@example.com').exists():
        raise ValidationError("A company with this contact email already exists.")

    if Company.objects.filter(phone_number='0400000000').exists():
        raise ValidationError("A company with this phone number already exists.")

    # Step 2: Create the company
    company = Company.objects.create(
        name='Example Admin Company',
        business_number='123456789',
        contact_email='admin@example.com',
        phone_number='0400000000',
        address='123 Admin St, City, Country'
    )

    # Step 3: Check if superuser exists
    if not User.objects.filter(username='admin').exists():
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        superuser.company = company
        superuser.save()

        # Step 4: Add to Admin group
        admin_group = Group.objects.get(name='BusinessOwner')
        superuser.groups.add(admin_group)

        print("Superuser created and linked to company and Admin group.")
    else:
        print("Admin user already exists.")
