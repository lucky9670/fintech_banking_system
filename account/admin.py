from django.contrib import admin
from account.models import *
# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'modified_at']

# admin.site.register(Role)
admin.site.register(Company)
admin.site.register(Scheme)
admin.site.register(Account)
admin.site.register(UserProfile)
