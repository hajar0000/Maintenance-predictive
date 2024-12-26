from rest_framework import serializers
from .models import Error, Failure, Telemetry, Machine, Maintenance

class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = '__all__'


class FailureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Failure
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = '__all__'

def serialize_telemetry_data(telemetries):
    serializer = TelemetrySerializer(telemetries, many=True)
    return serializer.data
