from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('super_distibuter', views.superDistibuter, name = "super_distibuter"),
    path('login', views.login, name = 'login'),
    path('register', views.registration, name = 'register'),
    path('logout', views.logout, name = 'logout'),
    path('scheme_manager', views.SchemeManager, name = 'scheme_manager'),
    path('role_manager', views.roleManager, name = 'role_manager'),
    path('company', views.company, name = 'company'),
    path('commission_type_manager', views.CommissionTypeManager, name = 'commission_type_manager'),
    path('api_manager', views.apiManager, name = 'api_manager'),
    path('provider_manager', views.ProviderManager, name = 'provider_manager'),
    path('delete_scheme', views.DeleteScheme, name = 'delete_scheme'),
    path('edit_scheme', views.editScheme, name = 'edit_scheme'),
    path('add_scheme', views.AddScheme, name = 'add_scheme'),
    path('delete_commission_type', views.DeleteCommssionType, name = 'delete_commission_type'),
    path('edit_commission_type', views.editCommissionType, name = 'edit_commission_type'),
    path('add_commission_type', views.AddCommissionType, name = 'add_commission_type'),
    path('whitelabel_management', views.AddScheme, name = 'whitelabel_management'),
    path('retailer_management', views.AddScheme, name = 'retailer_management'),
    path('super_dist_management', views.AddScheme, name = 'super_dist_management'),
    path('distributor_management', views.AddScheme, name = 'distributor_management'),
]
