from django.contrib import admin
from .models import Api, Consumer


class ApiAdmin(admin.ModelAdmin):
  list_display = ('request_path','upstream_url',  'get_consumers','description' )
  list_filter = ['consumers']
  search_fields = ['name', 'upstream_url']

  def get_consumers(self, obj):
    return ",".join([p.user.username for p in obj.consumers.all()])


class ConsumerAdmin(admin.ModelAdmin):
  list_display = ('user','description' )
  search_fields = ['user', 'description']

# Register your models here.
admin.site.register(Api, ApiAdmin)
admin.site.register(Consumer, ConsumerAdmin)