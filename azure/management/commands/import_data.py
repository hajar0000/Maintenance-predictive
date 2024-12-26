import csv
from django.core.management.base import BaseCommand
from datetime import datetime
import pytz
from django.conf import settings
from azure.models import Machine, Error, Failure, Maintenance, Telemetry


class Command(BaseCommand):
    help = 'Importe les données depuis des fichiers CSV'

    def handle(self, *args, **kwargs):
        # Import des machines
        self.import_machines('D:/django/man/PdM_machines.csv')

        # Import des erreurs
        self.import_errors('D:/django/man/PdM_errors.csv')

        # Import des pannes
        self.import_failures('D:/django/man/PdM_failures.csv')

        # Import des maintenances
        self.import_maintenance('D:/django/man/PdM_maint.csv')

        # Import des télémétries
        self.import_telemetry('D:/django/man/PdM_telemetry.csv')

    def import_machines(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                machine, created = Machine.objects.get_or_create(
                    machineID=row['machineID'],
                    defaults={
                        'model': row['model'],
                        'age': row['age']
                    }
                )
                if created:
                    self.stdout.write(f"Machine {machine.machineID} créée.")

    def import_errors(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Récupérer la machine à partir du machineID
                    machine = Machine.objects.get(machineID=row['machineID'])
                    
                    # Convertir la datetime pour être consciente du fuseau horaire UTC
                    naive_datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.UTC.localize(naive_datetime)  # Ajouter le fuseau horaire UTC

                    # Créer l'instance Error avec la datetime consciente du fuseau horaire
                    Error.objects.create(
                        datetime=aware_datetime,
                        machine=machine,
                        errorID=row['errorID']
                    )
                except Machine.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Machine avec l'ID {row['machineID']} introuvable."))

    def import_failures(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row.keys())  # Affichez les clés pour le débogage
                try:
                    # Assurez-vous que le nom correspond à celui du CSV
                    machine = Machine.objects.get(machineID=row['machineID'])  
                    
                    # Convertir la datetime pour être consciente du fuseau horaire UTC
                    naive_datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.UTC.localize(naive_datetime)

                    # Créer l'instance Failure avec la datetime consciente du fuseau horaire
                    Failure.objects.create(
                        datetime=aware_datetime,
                        machine=machine,
                        failure=row['failure']
                    )
                except Machine.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Machine avec l'ID {row['machineID']} introuvable."))


    def import_maintenance(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row.keys())  # Pour le débogage, voir les clés disponibles
                try:
                    machine = Machine.objects.get(machineID=row['machineID'])
                    
                    # Convertir la datetime pour être consciente du fuseau horaire UTC
                    naive_datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.UTC.localize(naive_datetime)

                    # Créer l'instance de maintenance sans maintenanceID
                    Maintenance.objects.create(
                        datetime=aware_datetime,
                        machine=machine,
                        comp=row['comp']  # Utilisez 'comp' à la place de 'maintenanceID'
                    )
                except Machine.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Machine avec l'ID {row['machineID']} introuvable."))
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"Clé introuvable dans le CSV: {e}"))


    def import_telemetry(self, file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row.keys())  # Pour le débogage
                try:
                    machine = Machine.objects.get(machineID=row['machineID'])  # Corrigez ici
                    naive_datetime = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
                    aware_datetime = pytz.UTC.localize(naive_datetime)
                    Telemetry.objects.create(
                        datetime=aware_datetime,
                        machine=machine,
                        volt=row['volt'],
                        rotate=row['rotate'],
                        pressure=row['pressure'],
                        vibration=row['vibration']
                    )
                    # Reste du code d'importation...
                except Machine.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Machine avec l'ID {row['machineID']} introuvable."))
                except KeyError as e:
                    self.stdout.write(self.style.ERROR(f"Clé introuvable dans le CSV: {e}"))

