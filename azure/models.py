from django.db import models

class Error(models.Model):
    datetime = models.DateTimeField()  # Correspond à la colonne 'datetime' dans le CSV
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)  # Correspond à 'machineID' via ForeignKey
    errorID = models.CharField(max_length=50)  # Correspond à la colonne 'errorID'

    def __str__(self):
        return f"{self.machine} - {self.errorID} at {self.datetime}"


class Failure(models.Model):
    datetime = models.DateTimeField()
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    failure = models.CharField(max_length=100)  # Failure category

    def __str__(self):
        return f"{self.machine} - {self.failure} at {self.datetime}"

class Machine(models.Model):
    machineID = models.CharField(max_length=50, primary_key=True)
    model = models.CharField(max_length=50)  # Category as CharField
    age = models.IntegerField()

    def __str__(self):
        return f"{self.machineID}"

class Maintenance(models.Model):
    datetime = models.DateTimeField()
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    comp = models.CharField(max_length=50)  # Component maintained

    def __str__(self):
        return f"{self.machine} - {self.comp} at {self.datetime}"

class Telemetry(models.Model):
    datetime = models.DateTimeField()
    machine = models.ForeignKey('Machine', on_delete=models.CASCADE)
    volt = models.FloatField()
    rotate = models.FloatField()
    pressure = models.FloatField()
    vibration = models.FloatField()

    def __str__(self):
        return f"Telemetry for {self.machine} at {self.datetime}"
