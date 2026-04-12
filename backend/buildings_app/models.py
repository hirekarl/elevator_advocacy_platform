from django.db import models
from django.db.models.functions import Now
from typing import Final

class Building(models.Model):
    """
    Represents an NYC Building mapped by its Building Identification Number (BIN).
    """
    bin = models.CharField(max_length=7, unique=True, primary_key=True)
    address = models.TextField()
    borough = models.CharField(max_length=20)
    created_at = models.DateTimeField(db_default=Now())

    def __str__(self) -> str:
        return f"{self.address} (BIN: {self.bin})"

class ElevatorReport(models.Model):
    """
    User-submitted reports for elevator status.
    Implements the 2-hour consensus logic.
    """
    STATUS_CHOICES: Final = [
        ('UP', 'Up'),
        ('DOWN', 'Down'),
    ]

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='reports')
    user_id = models.CharField(max_length=255)  # External user identifier
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    reported_at = models.DateTimeField(db_default=Now())
    
    # Metadata for SODA synchronization
    is_official = models.BooleanField(default=False)  # True if from SODA API
    soda_unique_key = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['building', 'reported_at', 'status']),
        ]

    def __str__(self) -> str:
        return f"{self.status} at {self.building.bin} by {self.user_id}"
