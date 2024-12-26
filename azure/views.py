from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Error, Failure, Machine, Maintenance, Telemetry
from .serializers import ErrorSerializer, FailureSerializer, MachineSerializer, MaintenanceSerializer, TelemetrySerializer, serialize_telemetry_data
from rest_framework.permissions import IsAuthenticated

class ErrorListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        if pk is None:
            errors = Error.objects.all()
            serializer = ErrorSerializer(errors, many=True)
            return Response(serializer.data)
        else:
            try:
                error = Error.objects.get(pk=pk)
                serializer = ErrorSerializer(error)
                return Response(serializer.data)
            except Error.DoesNotExist:
                raise Http404

    def post(self, request):
        serializer = ErrorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            serializer = ErrorSerializer(error, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Error.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            error.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Error.DoesNotExist:
            raise Http404
        

class FailureListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            failures = Failure.objects.all()
            serializer = FailureSerializer(failures, many=True)
            return Response(serializer.data)
        else:
            try:
                failure = Failure.objects.get(pk=pk)
                serializer = FailureSerializer(failure)
                return Response(serializer.data)
            except Failure.DoesNotExist:
                raise Http404

    def post(self, request):
        serializer = FailureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            failure = Failure.objects.get(pk=pk)
            serializer = FailureSerializer(failure, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Failure.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            failure = Failure.objects.get(pk=pk)
            failure.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Failure.DoesNotExist:
            raise Http404

class MachineListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            machines = Machine.objects.all()
            serializer = MachineSerializer(machines, many=True)
            return Response(serializer.data)
        else:
            try:
                machine = Machine.objects.get(pk=pk)
                serializer = MachineSerializer(machine)
                return Response(serializer.data)
            except Machine.DoesNotExist:
                raise Http404

    def post(self, request):
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            machine = Machine.objects.get(pk=pk)
            serializer = MachineSerializer(machine, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Machine.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            machine = Machine.objects.get(pk=pk)
            machine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Machine.DoesNotExist:
            raise Http404

class MaintenanceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is None:
            maintenances = Maintenance.objects.all()
            serializer = MaintenanceSerializer(maintenances, many=True)
            return Response(serializer.data)
        else:
            try:
                maintenance = Maintenance.objects.get(pk=pk)
                serializer = MaintenanceSerializer(maintenance)
                return Response(serializer.data)
            except Maintenance.DoesNotExist:
                raise Http404

    def post(self, request):
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            maintenance = Maintenance.objects.get(pk=pk)
            serializer = MaintenanceSerializer(maintenance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Maintenance.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        try:
            maintenance = Maintenance.objects.get(pk=pk)
            maintenance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Maintenance.DoesNotExist:
            raise Http404
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Telemetry, Machine
from .serializers import TelemetrySerializer

# Pagination class for Telemetry
class TelemetryPagination(PageNumberPagination):
    page_size = 100  # Number of records per page (adjust as needed).
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Set a reasonable limit for maximum records.

# Telemetry List View with Pagination, Filtering, and Caching
@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class TelemetryListCreateView(ListAPIView):
    serializer_class = TelemetrySerializer
    pagination_class = TelemetryPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the machine_id from query parameters (default to None if not provided)
        machine_id = self.request.query_params.get('machine_id', None)

        if machine_id:
            # Ensure the machine exists, and filter the Telemetry records accordingly
            try:
                machine = Machine.objects.get(machineID=machine_id)
            except Machine.DoesNotExist:
                # Return an empty queryset or raise an error if machine is not found
                return Telemetry.objects.none()  # Or you could raise a 404 error

            # Filter telemetry data based on the machine
            return Telemetry.objects.filter(machine=machine).order_by('-datetime')
        else:
            # If no machine_id is provided, return all telemetry data
            return Telemetry.objects.all().order_by('-datetime')

from django.shortcuts import render

def vis(request):
    return render(request, 'azure/vis.html')

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Error

class ErrorCountByMachineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, machine_id=None):
        if machine_id is None:
            return Response({'error': 'Machine ID is required'}, status=400)

        # Query to count each type of error for the given machine ID
        error_counts = (
            Error.objects.filter(machine_id=machine_id)
            .values('errorID')
            .annotate(count=Count('errorID'))
        )

        return Response(error_counts)

class MaintenanceCountByMachineView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, machine_id=None):
        if machine_id is None:
            return Response({'error': 'Machine ID is required'}, status=400)

        # Requête pour compter les maintenances par composant pour une machine donnée
        maintenance_counts = (
            Maintenance.objects.filter(machine=machine_id)
            .values('comp')
            .annotate(count=Count('id'))
        )

        return Response(maintenance_counts)
    

    