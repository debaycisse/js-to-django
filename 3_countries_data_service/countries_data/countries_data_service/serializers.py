from django.core.cache import cache
from os import getenv
from random import randint
from rest_framework import serializers
import requests
from countries_data.countries_data_service.models import Country


class CountryListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        '''
        creates and stores country instances

        Args:
            validated_data - a validated list of country data
        '''
        country_objects = []

        for data in validated_data:
            country_instance = Country(**data)
            if len(data.currencies) < 1:
                country_instance.currency_code = None
                country_instance.exchange_rate = None
                country_instance.estimated_gdp = 0.0
            else:
                currencies_rate = self.get_exchange_rate()
                currency_code = data.get('currencies')[0].get('code')
                exchange_rate = currencies_rate.get(currency_code, None)

                country_instance['currency_code'] = currency_code
                country_instance['exchange_rate'] = exchange_rate
                country_instance['estimated_gdp'] = self\
                    .get_estimated_gdp(
                        data.get('population'),
                        exchange_rate
                    ) if exchange_rate is not None else None
            
            country_objects.append(country_instance)
        
        return Country.objects.bulk_create(
            country_objects,
            update_conflicts=True,
            unique_fields=['name'], 
            update_fields=[
                'capital', 'region', 'population', 'currency_code',
                'exchange_rate', 'estimated_gdp', 'flag_url',
            ]
        )

    def get_estimated_gdp(self, population, exch_rate):
        '''
        computes and returns estimated gdp of a given population

        Args:
            population - the population value for
            the estimate to be computed

            exch_rate - the exchange rate with which
            the computation is done
        
        Returns:
            the float value of the computation
        '''
        rand_num = randint(1000, 2000)
        return population * rand_num / exch_rate
    
    def get_exchange_rate(self):
        '''
        calls an external exhcange rate api
        '''

        exchange_rate_cache_key = getenv('EXCHANGE_RATE_CACHE_KEY')
        exchange_rate_api = getenv('CURRENCY_API')
        cache_time_to_live = getenv('CACHE_TTL')

        exchange_rate_data = cache.get(exchange_rate_cache_key)

        if exchange_rate_data is None:

            exchange_rate_data = requests.get(
                exchange_rate_api,
                timeout=12
            ).json()

            cache.set(
                exchange_rate_cache_key,
                exchange_rate_data,
                cache_time_to_live
            )

        return exchange_rate_data.rates


# Country serializer
class CountrySerializer(serializers.ModelSerializer):
    currency_code = serializers.CharField(read_only=True)
    currencies = serializers.ListField(write_only=True)
    exchange_rate = serializers.FloatField(read_only=True)
    estimated_gdp = serializers.FloatField(read_only=True)
    last_refreshed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Country
        fields = [
            'id', 'name', 'capital', 'region', 'population',
            'currency_code', 'currencies', 'exchange_rate',
            'estimated_gdp', 'flag_url', 'last_refreshed_at'
        ]
        list_serializer_class = CountryListSerializer

    def to_representation(self, instance):
        output = super().to_representation(instance=instance)
        output['last_refreshed_at'] = instance\
            .last_refreshed_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        return output
