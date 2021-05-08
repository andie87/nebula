from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import Permission
from rest_admin.src.modules.auth.models import UserSecretKey, UserToken

# class PermissionAdmin(admin.ModelAdmin):
#     list_filter = ['content_type']
#     search_fields = ['name', 'codename']
#     pass

# class TokenAdmin(admin.ModelAdmin):
#     list_filter = ['user', 'created_by']
#     search_fields = ['user', 'token']
#     pass


# Register your models here.
# admin.site.register(UserSecretKey)
# admin.site.register(Permission, PermissionAdmin)
# admin.site.register(UserToken, TokenAdmin)




