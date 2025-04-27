from django.urls import path
from .views import CreateCompanyWithAdminView, CustomTokenObtainPairView, UserView

urlpatterns = [
    path('create-company/', CreateCompanyWithAdminView.as_view(), name='create_company_with_admin'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair_custom'),
    path('users/', UserView.as_view(), name='user_views'),

]