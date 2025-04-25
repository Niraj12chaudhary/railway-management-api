from rest_framework import serializers
from .models import Station, Train, Route, Booking

class StationSerializer(serializers.ModelSerializer):
    """Serializer for Station model
    
    Maps Station DB model to JSON representation
    """
    class Meta:
        model = Station
        fields = '__all__'

class TrainSerializer(serializers.ModelSerializer):
    """Serializer for Train model
    
    Handles train data serialization and validation
    """
    class Meta:
        model = Train
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    """Main route serializer with nested data fields
    
    Includes train and station name fields for frontend display
    """
    train_name = serializers.ReadOnlyField(source='train.name')
    source_name = serializers.ReadOnlyField(source='source.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')

    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ('available_seats',)  # Can only be updated via booking system

class RouteAvailabilitySerializer(serializers.ModelSerializer):
    """Route availability serializer
    
    Used for seat availability search results with extended fields
    """
    train_number = serializers.ReadOnlyField(source='train.train_number')
    train_name = serializers.ReadOnlyField(source='train.name')
    source_name = serializers.ReadOnlyField(source='source.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')
    
    class Meta:
        model = Route
        fields = ('id', 'train', 'train_number', 'train_name', 'source', 'source_name', 
                  'destination', 'destination_name', 'departure_time', 
                  'arrival_time', 'available_seats')

class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer with user and route details
    
    Handles data representation for ticket bookings
    """
    user_email = serializers.ReadOnlyField(source='user.email')
    train_name = serializers.ReadOnlyField(source='route.train.name')
    source_name = serializers.ReadOnlyField(source='route.source.name')
    destination_name = serializers.ReadOnlyField(source='route.destination.name')
    
    class Meta:
        model = Booking
        fields = ('booking_id', 'user', 'user_email', 'route', 'train_name', 
                  'source_name', 'destination_name', 'booking_time', 
                  'seat_number', 'status')
        read_only_fields = ('booking_id', 'user', 'user_email', 'booking_time', 'seat_number')

class BookTicketSerializer(serializers.Serializer):
    """Input validator for booking requests
    
    Validates route_id for booking API endpoint
    """
    route_id = serializers.IntegerField(required=True)
