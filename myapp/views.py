from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from collections import defaultdict
from rest_framework.response import Response
from .models import Landlord, Property, Room, Tenant, Electricity, Payment
from .serializers import LandlordSerializer, PropertySerializer, RoomSerializer, TenantSerializer, ElectricitySerializer, PaymentSerializer

class LandlordViewSet(viewsets.ModelViewSet):
    queryset = Landlord.objects.all()
    serializer_class = LandlordSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(detail=False, methods=['get'])
    def filter_by_reading_month(self, request):
        month = request.query_params.get('month')
        if not month or not month.isdigit():
            return Response({"error": "Please provide a valid month (1-12)."}, status=400)
        
        month = int(month)
        rooms = Room.objects.filter(reading_date=month).distinct()
        serializer = self.get_serializer(rooms, many=True)
        return Response(serializer.data)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class ElectricityViewSet(viewsets.ModelViewSet):
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

@api_view(['GET'])
def property_monthly_details(request, property_id, month):
    try:
        # Get all rooms under the given property
        rooms = Room.objects.filter(property_id=property_id)
        rooms_data = RoomSerializer(rooms, many=True).data

        # Get meter readings for the specified month
        meter_readings = Electricity.objects.filter(room__property_id=property_id, 
                                                     reading_date__month=month)
        meter_readings_data = ElectricitySerializer(meter_readings, many=True).data

        # Get payments for the specified month
        payments = Payment.objects.filter(room__property_id=property_id, month=month)
        payments_data = PaymentSerializer(payments, many=True).data

        # Organize data by room
        rooms_info = defaultdict(lambda: {"meter_readings": [], "payments": []})

        # Populate meter readings and payments for each room
        for reading in meter_readings_data:
            room_id = reading['room']
            rooms_info[room_id]['meter_readings'].append(reading)

        for payment in payments_data:
            room_id = payment['room']
            rooms_info[room_id]['payments'].append(payment)

        # Include room details as well
        room_details = {}
        for room in rooms_data:
            room_id = room['id']
            room_details[room_id] = {
                "room_number": room['room_number'],
                "is_occupied": room['is_occupied'],
                "meter_readings": rooms_info[room_id]['meter_readings'],
                "payments": rooms_info[room_id]['payments']
            }

        return Response(room_details)

    except Exception as e:
        return Response({"error": str(e)}, status=400)