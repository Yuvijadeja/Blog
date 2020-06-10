from django.db import models

# Create your models here.


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    date_join = models.DateField()


class Attempts(models.Model):
    email = models.CharField(max_length=100)
    attempts = models.IntegerField()
    attempt_time = models.TimeField()
