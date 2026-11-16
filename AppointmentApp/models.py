from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey('AccountApp.Doctor', on_delete=models.CASCADE, related_name='appointments')

    patient = models.ForeignKey('AccountApp.Patient', on_delete=models.CASCADE, related_name='appointments')

    reason=models.TextField()

    prescription=models.FileField(upload_to='prescriptions/',blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    appointment_date = models.DateTimeField()

    def clean(self):
        super().clean()

        if self.appointment_date:
            date_changed = True

            if self.pk:
                old_date = Appointment.objects.filter( pk=self.pk ).values_list('appointment_date', flat=True).first()

                if old_date == self.appointment_date:
                    date_changed = False

            if date_changed and self.appointment_date <= timezone.now():
                raise ValidationError({
                    'appointment_date': "La date du rendez-vous doit être dans le futur."
                })

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment_date',
                violation_error_message="Ce docteur possède un rdv avec cette date"
            )
        ]
        ordering = ['appointment_date']


