from django.urls import path
from .views import (
    StationView, TrainView, RouteView, TrainAvailabilityView,
    BookSeatView, BookingDetailView, UserBookingsView
)

urlpatterns = [
    # Admin endpoints (protected by API key)
    path('admin/stations/', StationView.as_view(), name='stations'),
    path('admin/trains/', TrainView.as_view(), name='trains'),
    path('admin/routes/', RouteView.as_view(), name='routes'),
    
    # User endpoints
    path('availability/', TrainAvailabilityView.as_view(), name='train_availability'),
    path('book/', BookSeatView.as_view(), name='book_seat'),
    path('bookings/', UserBookingsView.as_view(), name='user_bookings'),
    path('bookings/<uuid:booking_id>/', BookingDetailView.as_view(), name='booking_detail'),
]
