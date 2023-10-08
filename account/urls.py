from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('super_distibuter', views.superDistibuter, name = "super_distibuter"),
    path('login', views.login, name = 'login'),
    path('register', views.registration, name = 'register'),
    path('logout', views.logout, name = 'logout'),
]
# if settings.DEBUG:
#     urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
