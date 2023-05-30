from django.contrib import admin

from api.models import  Order, File

# Register your models here.
admin.site.register(Order)
admin.site.register(File)