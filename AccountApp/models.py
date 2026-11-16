from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    pass

def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError("La date de naissance doit être antérieure à aujourd'hui.")

class Doctor(User):

    license_number = models.CharField(max_length=6,unique=True,validators=[MinLengthValidator(6)])

    phone = models.CharField(max_length=8,validators=[RegexValidator(r'^\d{8}$')])

    specialties = models.ManyToManyField('Specialty',related_name='doctors')

class Patient(User):
    national_id=models.CharField(max_length=8,unique=True,validators=[RegexValidator(r'^\d{8}$')])
    phone=models.CharField(max_length=8,validators=[RegexValidator(r'^\d{8}$')])
    birth_date = models.DateField(validators=[validate_past_date])

class Specialty(models.Model):
    name=models.CharField(max_length=255)