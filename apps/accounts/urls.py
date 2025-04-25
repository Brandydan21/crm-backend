from django.urls import path
from .views import CreateCompanyWithAdminView

urlpatterns = [
    path('create-company/', CreateCompanyWithAdminView.as_view(), name='create_company_with_admin'),
]