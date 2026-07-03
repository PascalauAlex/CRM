from rest_framework import serializers
from .models import Address


class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            'country',
            'county',
            'city',
            'street',
            'street_number',
            'building',
            'floor',
            'apartment_number',
            'zipcode'

        )




