from rest_framework import serializers
from .models import Station, Train, Route, Booking

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'

class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    train_name = serializers.ReadOnlyField(source='train.name')
    source_name = serializers.ReadOnlyField(source='source.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')

    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ('available_seats',)

class RouteAvailabilitySerializer(serializers.ModelSerializer):
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
    route_id = serializers.IntegerField(required=True)
