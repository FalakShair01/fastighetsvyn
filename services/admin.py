from django.contrib import admin
from .models import (
    Development,
    UserDevelopmentServices,
    Maintenance,
    UserMaintenanceServices,
    ExternalSelfServices,
    SelfServiceProvider,
    ServiceDocument,
    ServiceDocumentFolder
)

# Register your models here.
admin.site.register(UserDevelopmentServices)
admin.site.register(Development)
admin.site.register(Maintenance)
admin.site.register(UserMaintenanceServices)
admin.site.register(ExternalSelfServices)
admin.site.register(SelfServiceProvider)
admin.site.register(ServiceDocumentFolder)
admin.site.register(ServiceDocument)
