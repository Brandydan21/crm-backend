from rest_framework import status, views
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.accounts.models import Company
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.accounts.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import BasePermission
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.db import transaction

User = get_user_model()

class CreateCompanyWithAdminView(views.APIView):
    permission_classes = [AllowAny] 

    """
    API endpoint to create a company and its initial admin user.
    """
    # atomic wraps the function, treating the function as one database
    # transaction, if one database transaction fails all fails and none 
    # are created
    @transaction.atomic
    def post(self, request):
        try:
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
            try:
                validate_password(password) 
            except DjangoValidationError as e:
                return Response({"password": list(e.messages)})  # raise DRF-friendly error

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
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                company=company,
                password=password
            )

            # Add to Admin group
            try:
                owner_group = Group.objects.get(name='BusinessOwner')
                user.groups.add(owner_group)
            except Group.DoesNotExist:
                return Response({"error": "BusinessOwner group not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            token = CustomTokenObtainPairSerializer.get_token(user)


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
                    "company": user.company.name,
                    'refresh': str(token),
                    'access': str(token.access_token)
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# login
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view that returns JWTs and user data including group and company info.
    """
    permission_classes = [AllowAny] 
    serializer_class = CustomTokenObtainPairSerializer




class UserView(views.APIView):
    permission_classes = [IsAuthenticated]

    allowed_groups = ['Admin', 'BusinessOwner', 'Manager']

    @transaction.atomic
    def post(self, request):
        try:
            user = request.user  

            # Get the authorised user's group permissions
            user_groups = list(user.groups.values_list('name', flat=True))
            
            # Get the authorised user's group permissions
            requested_role = request.data.get('role')


            if not requested_role:
                return Response({"error": "Role must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            if not any(group in self.allowed_groups for group in user_groups):
                return Response({"error": "You do not have permission to create users."}, status=status.HTTP_403_FORBIDDEN)
            
            if 'BusinessOwner' in user_groups:
                if requested_role not in ['BusinessOwner', 'Manager', 'Worker']:
                    return Response({"error": "BusinessOwner can only create BusinessOwner, Manager, or Worker roles."}, status=status.HTTP_403_FORBIDDEN)
            
            elif 'Manager' in user_groups:
                if requested_role != 'Worker':
                    return Response({"error": "Manager can only create Worker roles."}, status=status.HTTP_403_FORBIDDEN)
            
            if User.objects.filter(phone_number=request.data.get('phone_number')).exists():
                return Response({"error": "phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response({"error": " email already exists."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_password(request.data["password"]) 
            except DjangoValidationError as e:
                return Response({"password": list(e.messages)})  # raise DRF-friendly error
            
            request.data["company"] = user.company_id
            request.data["username"] = request.data["email"]
            
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True) 

            new_user = serializer.save() 

            try:
                group = Group.objects.get(name=requested_role)
                new_user.groups.add(group)  
            except Group.DoesNotExist:
                return Response({"error": " group not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
            return Response({
                "message": "User created successfully.",
                "user_id": new_user.id,
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "phone_number": new_user.phone_number,
                "company": new_user.company.name,
                "role": list(new_user.groups.values_list('name', flat=True))    
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)