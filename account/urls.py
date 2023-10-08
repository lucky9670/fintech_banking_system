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
]
