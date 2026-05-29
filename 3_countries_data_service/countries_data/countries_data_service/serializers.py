from rest_framework import serializers
from countries_data.countries_data_service.models import Country


class CountryListSerializer(serializers.ListSerializer):
    '''
    handles the creation of multiple countries data, using
    its create() method and hits the database once
    '''

    def create(self, validated_data):
        '''
        creates and stores country instances

        Args:
            validated_data - a validated list of country data
        '''

        country_objects = []

        for country in validated_data:
            country_instance = Country(**country)
            country_objects.append(country_instance)
        
        return Country.objects.bulk_create(
            country_objects,
            update_conflicts=True,
            update_fields=[
                'capital', 'region', 'population', 'currency_code',
                'exchange_rate', 'estimated_gdp', 'flag_url',
            ]
        )

# Country serializer
class CountrySerializer(serializers.ModelSerializer):
    '''
    handles both serialization and deserialization process
    for the country's instance and data
    '''

    name = serializers.CharField(validators=[])
    
    class Meta:
        model = Country
        fields = [
            'id', 'name', 'capital', 'region', 'population',
            'currency_code', 'exchange_rate', 'estimated_gdp',
            'flag_url', 'last_refreshed_at'
        ]
        list_serializer_class = CountryListSerializer

    def to_representation(self, instance):
        if instance.last_refreshed_at:

            instance.last_refreshed_at = instance\
                .last_refreshed_at.strftime('%Y-%m-%dT%H:%M:%SZ')

        return super().to_representation(instance=instance)
