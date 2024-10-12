from django.contrib import admin
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    OrderMaintenanceServices,
    ExternalSelfServices,
    SelfServiceProvider,
    ServiceFile,
    ServiceDocumentFolder
)

# Register your models here.
admin.site.register(UserDevelopmentServices)
admin.site.register(Development)
admin.site.register(Maintenance)
admin.site.register(OrderMaintenanceServices)
admin.site.register(ExternalSelfServices)
admin.site.register(SelfServiceProvider)
admin.site.register(ServiceDocumentFolder)
admin.site.register(ServiceFile)
