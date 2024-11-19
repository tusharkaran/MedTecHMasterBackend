from django.db import models


class Alert(models.Model):
    patient = models.CharField(max_length=255)
    doctor = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    severity = models.CharField(max_length=50, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical')
    ])
    description = models.TextField()

    class Meta:
        db_table = 'alerts'
        ordering = ['-timestamp']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

    def __str__(self):
        return f"Alert({self.patient}, {self.doctor}, {self.severity})"

    @classmethod
    def create_alert(cls, patient, doctor, timestamp, severity, description):
        """
        Create a new alert and save it to the database.
        """
        alert = cls.objects.create(
            patient=patient,
            doctor=doctor,
            timestamp=timestamp,
            severity=severity,
            description=description
        )
        return alert

    @classmethod
    def get_alert_by_id(cls, alert_id):
        """
        Retrieve an alert by its ID.
        """
        try:
            return cls.objects.get(id=alert_id)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_all_alerts(cls):
        """
        Retrieve all alerts from the database.
        """
        return cls.objects.all()
