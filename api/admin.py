from django.contrib import admin

from api.models import  Order, File

# Register your models here.
admin.site.register(File)
class OrderAdmin(admin.ModelAdmin):
    list_display= ('id', 'nom',)
    readonly_fields= ('id',)

admin.site.register(Order, OrderAdmin)
