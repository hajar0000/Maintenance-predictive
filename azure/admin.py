from django.contrib import admin

from .models import Error, Failure, Machine, Maintenance, Telemetry

admin.site.register(Error)
admin.site.register(Maintenance)
admin.site.register(Machine)
admin.site.register(Telemetry)
admin.site.register(Failure)