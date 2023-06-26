from django.contrib import admin

from api.models import  Order, File

# Register your models here.
admin.site.register(File)
class OrderAdmin(admin.ModelAdmin):
    list_display= ('id', 'nom','create_dt' ,'modify_dt',)
    readonly_fields= ('id','create_dt','modify_dt','order_number')

admin.site.register(Order, OrderAdmin)
