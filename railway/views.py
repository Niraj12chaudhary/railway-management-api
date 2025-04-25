from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Station, Train, Route, Booking
from .serializers import (
    StationSerializer, TrainSerializer, RouteSerializer, 
    RouteAvailabilitySerializer, BookingSerializer, BookTicketSerializer
)

# Custom permission classes
class IsAdminUser(permissions.BasePermission):
    """Checks if user is authenticated and has admin privileges."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class AdminAPIKeyPermission(permissions.BasePermission):
    """Validates API key in request header."""
    def has_permission(self, request, view):
        # In Django, X-API-KEY becomes HTTP_X_API_KEY in request.META
        api_key_header = 'HTTP_' + settings.API_KEY_HEADER.replace('-', '_').upper()
        api_key = request.META.get(api_key_header)
        return api_key == settings.API_KEY

# Admin API endpoints
class StationView(APIView):
    """Handles CRUD operations for stations."""
    permission_classes = [IsAuthenticated, IsAdminUser, AdminAPIKeyPermission]
    
    def post(self, request):
        """Creates a new station."""
        serializer = StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Retrieves all stations."""
        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
        return Response(serializer.data)

class TrainView(APIView):
    """Handles CRUD operations for trains."""
    permission_classes = [IsAuthenticated, IsAdminUser, AdminAPIKeyPermission]
    
    def post(self, request):
        """Creates a new train."""
        serializer = TrainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Retrieves all trains."""
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data)

class RouteView(APIView):
    """Handles CRUD operations for routes."""
    permission_classes = [IsAuthenticated, IsAdminUser, AdminAPIKeyPermission]
    
    def post(self, request):
        """Creates a new route."""
        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            # Initialize available seats to train's total seats
            train = Train.objects.get(pk=serializer.validated_data['train'].id)
            serializer.validated_data['available_seats'] = train.total_seats
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """Retrieves all routes."""
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

# User API endpoints
class TrainAvailabilityView(APIView):
    """Checks train availability between source and destination."""
    def get(self, request):
        source_id = request.query_params.get('source')
        destination_id = request.query_params.get('destination')
        
        if not source_id or not destination_id:
            return Response(
                {"error": "Both source and destination are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        routes = Route.objects.filter(
            source_id=source_id, 
            destination_id=destination_id,
            available_seats__gt=0
        )
        
        serializer = RouteAvailabilitySerializer(routes, many=True)
        return Response(serializer.data)

class BookSeatView(APIView):
    """Books a seat on a train."""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = BookTicketSerializer(data=request.data)
        if serializer.is_valid():
            route_id = serializer.validated_data['route_id']
            
            try:
                # Use a transaction with select_for_update to prevent race conditions
                with transaction.atomic():
                    # Lock the route record to prevent concurrent modifications
                    route = Route.objects.select_for_update().get(pk=route_id)
                    
                    # Check if seats are available
                    if route.available_seats <= 0:
                        return Response(
                            {"error": "No seats available for this route"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Find the next available seat number
                    existing_bookings = Booking.objects.filter(route=route, status='CONFIRMED')
                    booked_seats = set(booking.seat_number for booking in existing_bookings)
                    
                    # Find first available seat (simple algorithm)
                    train_total_seats = route.train.total_seats
                    seat_number = None
                    for i in range(1, train_total_seats + 1):
                        if i not in booked_seats:
                            seat_number = i
                            break
                    
                    if seat_number is None:
                        return Response(
                            {"error": "No available seat found"}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Create booking
                    booking = Booking.objects.create(
                        user=request.user,
                        route=route,
                        seat_number=seat_number,
                        status='CONFIRMED'
                    )
                    
                    # Update available seats
                    route.available_seats -= 1
                    route.save()
                    
                    return Response(
                        BookingSerializer(booking).data, 
                        status=status.HTTP_201_CREATED
                    )
                    
            except Route.DoesNotExist:
                return Response(
                    {"error": "Route not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except IntegrityError:
                return Response(
                    {"error": "Failed to book seat. Please try again."}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingDetailView(APIView):
    """Retrieves details of a specific booking."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UserBookingsView(APIView):
    """Retrieves all bookings of a user."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
