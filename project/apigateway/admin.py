from django.contrib import admin
from .models import Api, Consumer
from django.db.models import Q


class ApiAdmin(admin.ModelAdmin):
  list_display = ('request_path','upstream_url',  'get_consumers','description', 'created_by' )
  list_filter = ['consumers']
  search_fields = ['name', 'upstream_url']
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
      return qs.filter(Q(created_by=request.user)|Q(consumers__in=user))

    else:
      return qs

  def has_change_permission(self, request, obj=None):
    if not obj:
      # the changelist itself
      return True
    return obj.created_by == request.user


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
      return qs.filter(Q(created_by=request.user)|Q(user__username=request.user))
    else:
      return qs

  def has_change_permission(self, request, obj=None):
    if not obj:
      # the changelist itself
      return True
    return obj.created_by == request.user

# Register your models here.
admin.site.register(Api, ApiAdmin)
admin.site.register(Consumer, ConsumerAdmin)