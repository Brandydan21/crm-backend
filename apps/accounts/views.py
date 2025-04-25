from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.accounts.models import Company
from rest_framework.permissions import AllowAny

User = get_user_model()

class CreateCompanyWithAdminView(views.APIView):
    permission_classes = [AllowAny]  # ✅ make it public

    """
    API endpoint to create a company and its initial admin user.
    """
    def post(self, request):
        data = request.data

        # Extract company data
        name = data.get('name')
        business_number = data.get('business_number')
        company_email = data.get('company_email')
        company_phone_number = data.get('company_phone_number')
        company_address = data.get('company_address')

        # Extract admin user data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')

        # Validate required fields
        if not all([name, business_number, company_email, company_phone_number, company_address, first_name, last_name, email, phone_number, password]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check for unique constraints
        if Company.objects.filter(business_number=business_number).exists():
            return Response({"error": "Business number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if Company.objects.filter(company_email=company_email).exists():
            return Response({"error": "Company email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if Company.objects.filter(company_phone_number=company_phone_number).exists():
            return Response({"error": "Company phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"error": "User email already in use."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "User phone number already in use."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the company
        company = Company.objects.create(
            name=name,
            business_number=business_number,
            company_email=company_email,
            company_phone_number=company_phone_number,
            company_address=company_address
        )

        # Create the admin user and assign company
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            company=company
        )

        # Add to Admin group
        try:
            owner_group = Group.objects.get(name='BusinessOwner')
            user.groups.add(owner_group)
        except Group.DoesNotExist:
            return Response({"error": "BusinessOwner group not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
        "message": "Company and admin user created successfully.",
        "company": {
            "id": company.id,
            "name": company.name,
            "business_number": company.business_number,
            "contact_email": company.company_email,
            "phone_number": company.company_phone_number,
            "address": company.company_address,
        },
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "company": user.company.name
        }
    }, status=status.HTTP_201_CREATED)
