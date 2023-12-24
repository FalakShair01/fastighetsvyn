from django.contrib import admin
from .models import Development, UserDevelopmentServices, Maintenance

# Register your models here.
admin.site.register(UserDevelopmentServices)
admin.site.register(Development)
admin.site.register(Maintenance)