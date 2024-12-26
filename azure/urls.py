from django.urls import path
from .views import ErrorCountByMachineView
from .views import MaintenanceCountByMachineView
from .views import (
    ErrorListCreateView,
    FailureListCreateView,
    MachineListCreateView,
    MaintenanceListCreateView,
    TelemetryListCreateView,
    vis,
)

urlpatterns = [
    path('', vis, name='vis'),

    path('errors/', ErrorListCreateView.as_view(), name='error-list-create'),
    path('errors/<int:pk>/', ErrorListCreateView.as_view(), name='error-detail'),
    path('errors/<int:machine_id>/count/', ErrorCountByMachineView.as_view(), name='error-count-by-machine'),

    

    path('failures/', FailureListCreateView.as_view(), name='failure-list-create'),
    path('failures/<int:pk>/', FailureListCreateView.as_view(), name='failure-detail'),
    

    path('machines/', MachineListCreateView.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', MachineListCreateView.as_view(), name='machine-detail'),

    path('maintenances/', MaintenanceListCreateView.as_view(), name='maintenance-list-create'),
    path('maintenances/<int:pk>/', MaintenanceListCreateView.as_view(), name='maintenance-detail'),
    path('maintenances/<int:machine_id>/count/', MaintenanceCountByMachineView.as_view(), name='maintenance-count-by-machine'),


    path('telemetries/', TelemetryListCreateView.as_view(), name='telemetry-list-create'),
]
