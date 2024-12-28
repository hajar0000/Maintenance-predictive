from django.urls import path
from .views import ErrorCountByMachineView
from .views import MaintenanceCountByMachineView
from .views import FailureDistributionView
from .views import machine_predictions_view
from .views import daily_errors_view
from .views import mtbf_view
from .views import (
    ErrorListCreateView,
    FailureListCreateView,
    MachineListCreateView,
    MaintenanceListCreateView,
    TelemetryListCreateView,
    vis,
    global_view,
    
)

urlpatterns = [
    path('', global_view, name='global'), 
    path('predictions/', machine_predictions_view, name='machine_predictions'), 
    path('machine/', vis, name='vis'),

    path('errors/', ErrorListCreateView.as_view(), name='error-list-create'),
    path('errors/<int:pk>/', ErrorListCreateView.as_view(), name='error-detail'),
    path('errors/<int:machine_id>/count/', ErrorCountByMachineView.as_view(), name='error-count-by-machine'),
    path('errors_today/', daily_errors_view, name='daily_errors'),

    

    path('failures/', FailureListCreateView.as_view(), name='failure-list-create'),
    path('failures/<int:pk>/', FailureListCreateView.as_view(), name='failure-detail'),
    path('failure-distribution/', FailureDistributionView.as_view(), name='failure-distribution'),
    

    path('machines/', MachineListCreateView.as_view(), name='machine-list-create'),
    path('machines/<int:pk>/', MachineListCreateView.as_view(), name='machine-detail'),

    path('maintenances/', MaintenanceListCreateView.as_view(), name='maintenance-list-create'),
    path('maintenances/<int:pk>/', MaintenanceListCreateView.as_view(), name='maintenance-detail'),
    path('maintenances/<int:machine_id>/count/', MaintenanceCountByMachineView.as_view(), name='maintenance-count-by-machine'),
    path('mtbf/', mtbf_view, name='mtbf'),


    path('telemetries/', TelemetryListCreateView.as_view(), name='telemetry-list-create'),
]
