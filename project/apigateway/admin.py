from django.contrib import admin
from .models import Api, Consumer
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class MyUserAdmin(UserAdmin):
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff', 'groups','user_permissions' )

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]

class ApiAdmin(admin.ModelAdmin):
  list_display = ('request_path','exposed_url',  'get_consumers','description', 'created_by' )
  list_filter = ['consumers']
  search_fields = ['name', 'description', 'request_path']
  exclude = ('created_by','modified_by',)

  def get_consumers(self, obj):
    return ",".join([p.user.username for p in obj.consumers.all()])

  def save_form(self, request, form, change):
    obj = super().save_form(request, form, change)
    if not change:
      obj.created_by = request.user

    if change:
      obj.modified_by = request.user

    return obj

  def get_queryset(self, request):
    qs = super(ApiAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      user = Consumer.objects.filter(user__username=request.user)
      return qs.filter(Q(created_by=request.user)|Q(consumers__in=user)).distinct("id")

    else:
      return qs

  def has_change_permission(self, request, obj=None):
    if request.user.is_superuser:
      return True
    return super(ApiAdmin, self).has_change_permission(request)


  def has_delete_permission(self, request, obj=None):
    if request.user.is_superuser:
      return True
    return super(ApiAdmin, self).has_delete_permission(request)


class ConsumerAdmin(admin.ModelAdmin):
  list_display = ('user','description', 'created_by', 'modified_by'  )
  search_fields = ['user', 'description']
  exclude = ('created_by','modified_by',)

  def save_form(self, request, form, change):
    obj = super().save_form(request, form, change)
    if not change:
      obj.created_by = request.user

    if change:
      obj.modified_by = request.user

    return obj

  def get_queryset(self, request):
    qs = super(ConsumerAdmin, self).get_queryset(request)
    if not request.user.is_superuser:
      return qs.filter(Q(created_by=request.user)|Q(user__username=request.user)).distinct("id")
    else:
      return qs

  def has_change_permission(self, request, obj=None):
    if request.user.is_superuser:
      return True
    return super(ConsumerAdmin, self).has_change_permission(request)


  def has_delete_permission(self, request, obj=None):
    if request.user.is_superuser:
      return True
    return super(ConsumerAdmin, self).has_delete_permission(request)

# Register your models here.
admin.site.register(Api, ApiAdmin)
admin.site.register(Consumer, ConsumerAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.site_header  =  "Nebula Gateway Administration"