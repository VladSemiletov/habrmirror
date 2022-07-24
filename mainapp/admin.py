from django.contrib import admin
from mainapp.models import HabCategory, Hab

# Register your models here.
admin.site.register(Hab)
admin.site.register(HabCategory)