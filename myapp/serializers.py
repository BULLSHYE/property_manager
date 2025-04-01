from rest_framework import serializers
from .models import Landlord, Property, Room, Tenant, Electricity, Payment

class LandlordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landlord
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

    def validate(self, data):
        landlord = data.get('landlord')
        if not landlord.is_subscription and Property.objects.filter(landlord=landlord).count() >=1:
            raise serializers.ValidationError("Non subscribed landlords")
        # return super().validate(data)
        return data

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
    
    def validate(self, data):
        landlord = data['property'].landlord
        if not landlord.is_subscription and Room.objects.filter(property__landlord=landlord).count() >= 1:
            raise serializers.ValidationError("Non-subscribed landlords can only have one room.")
        return data

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

class ElectricitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Electricity
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
