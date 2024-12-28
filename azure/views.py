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

from django.shortcuts import render

# Vue pour la page globale
def global_view(request):
    return render(request, 'azure/global.html')

# Vue pour la page vis
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
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Failure
from .serializers import FailureSerializer
from rest_framework.permissions import IsAuthenticated
import numpy as np
from scipy.stats import kstest, norm, expon, weibull_min, uniform

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Failure
from .serializers import FailureSerializer
from rest_framework.permissions import IsAuthenticated
import numpy as np
from scipy.stats import kstest, norm, expon, weibull_min, uniform
from datetime import datetime

class FailureDistributionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        machine_id = request.query_params.get('machine_id')
        if machine_id is None:
            return Response({'error': 'Machine ID is required'}, status=400)
        
        failures = Failure.objects.filter(machine_id=machine_id).order_by('datetime')
        if not failures.exists():
            return Response({'error': 'No failures found for this machine'}, status=404)

        serializer = FailureSerializer(failures, many=True)
        
        # Convert datetime string to datetime objects and then to timestamps
        timestamps = np.array([datetime.fromisoformat(failure['datetime']).timestamp() for failure in serializer.data])

        # Test for Normal distribution
        mu, std = norm.fit(timestamps)
        stat_norm, p_norm = kstest(timestamps, 'norm', args=(mu, std))
        
        # Test for Exponential distribution
        stat_exp, p_exp = kstest(timestamps, expon.cdf)
        
        # Test for Weibull distribution
        shape_weib, loc_weib, scale_weib = weibull_min.fit(timestamps)
        stat_weib, p_weib = kstest(timestamps, 'weibull_min', args=(shape_weib, loc_weib, scale_weib))
        
        # Test for Uniform distribution
        stat_uni, p_uni = kstest(timestamps, uniform.cdf)
        
        distributions = [
            {'name': 'Normale', 'p_value': p_norm},
            {'name': 'Exponentielle', 'p_value': p_exp},
            {'name': 'Weibull', 'p_value': p_weib},
            {'name': 'Uniforme', 'p_value': p_uni}
        ]
        
        return JsonResponse({
            'distributions': distributions,
            'failures': serializer.data
        })

import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from sklearn.preprocessing import MinMaxScaler
from .models import Telemetry, Machine
import logging

logger = logging.getLogger(__name__)

# Example dataset to fit the scaler
example_data = pd.DataFrame({
    'age': [0, 21],
    'volt': [100, 240],
    'rotate': [0, 500],
    'pressure': [0, 200],
    'vibration': [0, 50],
    'time_step': [1, 10]
})
scaler = MinMaxScaler()
scaler.fit(example_data)

def machine_predictions_view(request):
    logger.info("Machine predictions view called")

    try:
        # Load the pre-trained model
        logger.info("Loading model")
        linear_model = joblib.load('D:/django/man/linear_model.pkl')
        logger.info("Model loaded successfully")

        # Fetch all machines
        machines = Machine.objects.all()
        results = []

        for machine in machines:
            try:
                logger.info(f"Processing machine: {machine.machineID}")
                
                # Fetch the latest telemetry data for the current machine
                latest_telemetry = Telemetry.objects.filter(machine=machine.machineID).latest('datetime')
                logger.info(f"Latest telemetry data for machine {machine.machineID}: {latest_telemetry}")

                # Prepare the data for prediction
                telemetry_data = {
                    'datetime': [latest_telemetry.datetime],
                    'age': [machine.age],
                    'volt': [latest_telemetry.volt],
                    'rotate': [latest_telemetry.rotate],
                    'pressure': [latest_telemetry.pressure],
                    'vibration': [latest_telemetry.vibration]
                }
                new_data = pd.DataFrame(telemetry_data)
                logger.info(f"New data prepared for machine {machine.machineID}: {new_data}")

                # Convert datetime values to timestamps and calculate time_step
                new_data['timestamp'] = new_data['datetime'].apply(lambda x: datetime.timestamp(x))
                new_data['time_step'] = [1]
                logger.info(f"Data with timestamps and time_step for machine {machine.machineID}: {new_data}")

                # Normalize the data using pre-fitted scaler
                new_data_normalized = scaler.transform(new_data[['age', 'volt', 'rotate', 'pressure', 'vibration', 'time_step']])
                logger.info(f"Data normalized for machine {machine.machineID}: {new_data_normalized}")

                # Log the input to the model
                logger.info(f"Input to model for machine {machine.machineID}: {new_data_normalized}")

                # Make the prediction
                prediction = linear_model.predict(new_data_normalized)
                seconds_to_fail = prediction[0]
                logger.info(f"Prediction for machine {machine.machineID}: {seconds_to_fail}")

                # Add prediction details to the results
                results.append({
                    'machine_id': machine.machineID,
                    'seconds_to_fail': seconds_to_fail,
                    'time_step': new_data['time_step'].tolist()
                })
            except Exception as e:
                logger.error(f"Error processing machine {machine.machineID}: {e}")
                continue

        # Sort results by time to fail
        results.sort(key=lambda x: x['seconds_to_fail'])

        return JsonResponse({'predictions': results})
    except Exception as e:
        logger.error(f"Error in machine predictions view: {e}")
        return JsonResponse({'error': str(e)}, status=500)

from django.utils import timezone
from .models import Error

def daily_errors_view(request):
    today = timezone.now().date()
    errors_today = Error.objects.filter(datetime__date=today)

    errors_list = [
        {
            'machine_id': error.machine.machineID,
            'timestamp': error.datetime,
            'error_id': error.errorID
        }
        for error in errors_today
    ]

    return JsonResponse({'errors_today': errors_list})


from django.utils import timezone
from django.db.models import Max, Min
from .models import Maintenance, Machine

def mtbf_view(request):
    machines = Machine.objects.all()
    results = []

    for machine in machines:
        maintenances = Maintenance.objects.filter(machine=machine.machineID)
        if maintenances.exists():
            num_failures = maintenances.count()

            first_maintenance = maintenances.aggregate(Min('datetime'))['datetime__min']
            last_maintenance = maintenances.aggregate(Max('datetime'))['datetime__max']
            total_operation_time = (last_maintenance - first_maintenance).total_seconds() / 3600.0

            mtbf = total_operation_time / num_failures
            failure_rate = num_failures / total_operation_time  # Calcul du taux de défaillance

            # Fiabilité à 1 heure
            reliability = 2.71828 ** (-failure_rate * 1)  # Utilisation de exp(-λt)

            results.append({
                'machine_id': machine.machineID,
                'mtbf': mtbf,
                'failure_rate': failure_rate,
                'reliability': reliability
            })
    
    return JsonResponse({'mtbf': results})
