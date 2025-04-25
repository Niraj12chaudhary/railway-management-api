from django.contrib import admin
from .models import Station, Train, Route, Booking

# Register your models here.
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city')
    search_fields = ('name', 'code', 'city')

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'train_number', 'total_seats')
    search_fields = ('name', 'train_number')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('train', 'source', 'destination', 'departure_time', 'arrival_time', 'available_seats')
    list_filter = ('train', 'source', 'destination')
    search_fields = ('train__name', 'source__name', 'destination__name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'route', 'booking_time', 'seat_number', 'status')
    list_filter = ('status', 'booking_time')
    search_fields = ('booking_id', 'user__email', 'route__train__name')
    readonly_fields = ('booking_id', 'booking_time')
