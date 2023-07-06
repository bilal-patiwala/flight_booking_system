from .models import User, Flight, Ticket
from rest_framework import serializers


class FlightUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','is_flight_user', 'is_active']

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        user.is_active = True
        user.is_flight_user = True
        user.save()
        return user

class FlightAdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','is_flight_admin', 'is_active']

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        user.is_active = True
        user.is_flight_admin = True
        user.save()
        return user

class AddFlightSerializer(serializers.ModelSerializer):
    total_seats_left = serializers.IntegerField(required=False)
    class Meta:
        model = Flight
        fields = "__all__"

    def create(self, validated_data):
        flight = Flight.objects.create(**validated_data)
        flight.save()
        return flight

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields = "__all__"


class GetFlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["id", "origin_country", "origin_city", "destination_country", "destination_city", "departure_time", "departure_date", "total_seats_left", "price"]

class GetBookedTicketsSerializer(serializers.ModelSerializer):
    flight_id = serializers.PrimaryKeyRelatedField(source="flight.id", read_only=True)
    origin_country = serializers.PrimaryKeyRelatedField(source="flight.origin_country", read_only=True)
    origin_city = serializers.PrimaryKeyRelatedField(source="flight.origin_city", read_only=True)
    destination_country = serializers.PrimaryKeyRelatedField(source="flight.destination_country", read_only=True)
    destination_city = serializers.PrimaryKeyRelatedField(source="flight.destination_city", read_only=True)
    departure_time = serializers.PrimaryKeyRelatedField(source="flight.departure_time", read_only=True)
    departure_date = serializers.PrimaryKeyRelatedField(source="flight.departure_date", read_only=True)
    price = serializers.PrimaryKeyRelatedField(source="flight.price", read_only=True)
    passenger = serializers.PrimaryKeyRelatedField(source="passenger.username", read_only=True)

    class Meta:
        model = Ticket
        fields = ['id','origin_country', "origin_city", "destination_country", "destination_city", "departure_time", "departure_date","price", "booking_date", "passenger", "flight_id"]