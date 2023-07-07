from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, APIView, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, Flight, Ticket
from .serializers import FlightUserRegisterSerializer, FlightAdminRegisterSerializer, AddFlightSerializer, TicketSerializer, GetFlightSerializer, GetBookedTicketsSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import datetime
User = get_user_model()

# Create your views here.

# class FlightsTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token['username'] = user.username
#         token['id'] = user.id
#         token['is_flight_user'] = user.is_flight_user
#         token['is_flight_admin'] = user.is_flight_admin
#         return token

# class FlightsTokenObtainPairView(TokenObtainPairView):
#     serializer_class = FlightsTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def FlightUserLogin(request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid Username or Password'}, status=401)
        
        if user.is_flight_user == False:
            return Response({'error': 'not a user'}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access': access_token, 'refresh':str(refresh)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def FlightAdminLogin(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid Username or Password'}, status=401)

        
        if user.is_flight_admin == False:
            return Response({'error': 'not a admin'}, status=401)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access': access_token, 'refresh':str(refresh)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([])
def flight_user_register(request):
    data = request.data
    username = data['username']
    email = data['email']
    in_validation = {}
    if User.objects.filter(username=username).exists():
        return Response({'error':"username alredy registered"},status=status.HTTP_409_CONFLICT)
    if User.objects.filter(email=email).exists():
        return Response({'error':"email is alredy registered"}, status=status.HTTP_409_CONFLICT)

    serializer = FlightUserRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([])
def flight_admin_register(request):
    data = request.data
    username = data['username']
    email = data['email']
    in_validation = {}
    if User.objects.filter(username=username).exists():
        return Response({'error':"username alredy registered"},status=status.HTTP_409_CONFLICT)
    if User.objects.filter(email=email).exists():
        return Response({'error':"email is alredy registered"}, status=status.HTTP_409_CONFLICT)

    serializer = FlightAdminRegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status":status.HTTP_201_CREATED})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
@permission_classes([])
def  addflight(request):
    data = request.data
    print(data)
    serializer = AddFlightSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([])
def deleteFlight(request, id):
    flight = Flight.objects.filter(id=id)
    flight.delete()
    return Response({"status":status.HTTP_204_NO_CONTENT})

@api_view(['POST'])
@permission_classes([])
def bookTicket(request):
    token = request.headers.get('Authorization').split()[1]
    decoded_token = RefreshToken(token)
    user_id = decoded_token.payload.get('user_id')
    data = request.data
    flight_id = data['flight_id']
    flight = Flight.objects.filter(id=flight_id).first()
    if flight.total_seats_left == 0:
        return Response({"message":"All tickets have been sold out"})
    seat_number = 60 - (flight.total_seats_left-1)
    context = {
        'flight':flight_id,
        'passenger':user_id,
        'seat_number':seat_number,
        'price':flight.price
    }
    serializer = TicketSerializer(data=context)
    if serializer.is_valid():
        flight.total_seats_left -= 1
        flight.save()
        serializer.save()
        return Response({'status':status.HTTP_201_CREATED})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([])
def getFlights(request):
    try:
        origin_country = request.GET.get('origin')
        destination_country = request.GET.get('destination')
        date = request.GET.get('date')
        time = request.GET.get('time')

        flights = Flight.objects.all()
        if origin_country:
            flights = flights.filter(origin_country__iexact=origin_country)
        if destination_country:
            flights = flights.filter(destination_country__iexact=destination_country)
        if date:
            flights = flights.filter(departure_date=date)
        if time:
            flights = flights.filter(departure_time=time)

        serializer = GetFlightSerializer(flights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([])
def user_booked_tickets(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        decoded_token = RefreshToken(token)
        user_id = decoded_token.payload.get('user_id')
        tickets = Ticket.objects.filter(passenger=user_id).order_by("-booking_date")
        print(tickets)
        serializer = GetBookedTicketsSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([])
def getFlightsForAdmin(request):
    try:
        flightno = request.GET.get('flightno')
        time = request.GET.get('time')

        if flightno:
            ticket = Ticket.objects.filter(flight=flightno)
        if time:
            flight = Flight.objects.filter(departure_time=time).first()
            ticket = Ticket.objects.filter(flight=flight.id)

        serializer = GetBookedTicketsSerializer(ticket, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({"status":status.HTTP_400_BAD_REQUEST})

@api_view(['GET'])
@permission_classes([])
def getsingleFlights(request):
    try:
        flight_id = request.GET.get('flightno')

        flights = Flight.objects.filter(id=flight_id).first()

        serializer = GetFlightSerializer(flights)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


