from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid

# DB models for railway management system

class Station(models.Model):
    """Station entity with unique identifiers"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # Station code (e.g. NDLS for New Delhi)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class Train(models.Model):
    """Train entity with capacity info"""
    name = models.CharField(max_length=100)
    train_number = models.CharField(max_length=20, unique=True)  # Unique identifier
    total_seats = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} ({self.train_number})"

class Route(models.Model):
    """Route mapping between stations with schedule data"""
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name='routes')
    source = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='departures')
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='arrivals')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('train', 'source', 'destination', 'departure_time')
    
    def __str__(self):
        return f"{self.train.name}: {self.source.code} to {self.destination.code}"
    
    def clean(self):
        # Validate time consistency
        if self.arrival_time <= self.departure_time:
            raise ValidationError("Arrival time must be after departure time")
        
        # Validate route logic
        if self.source == self.destination:
            raise ValidationError("Source and destination stations cannot be the same")
    
    def save(self, *args, **kwargs):
        # Initialize seat count if not provided
        if not self.pk and self.available_seats is None:
            self.available_seats = self.train.total_seats
        self.clean()
        super().save(*args, **kwargs)

class Booking(models.Model):
    """Booking entity with user and route info"""
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='bookings')
    booking_time = models.DateTimeField(auto_now_add=True)
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('WAITING', 'Waiting')
    ], default='CONFIRMED')
    
    class Meta:
        unique_together = ('route', 'seat_number')
    
    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.email}"
