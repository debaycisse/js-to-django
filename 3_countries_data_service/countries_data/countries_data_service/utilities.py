from django.core.cache import cache
from os import getenv
import requests
from random import randint


def get_countries_or_currency(**kwargs):

    '''
    calls currency exchange rate or countries api, 
    depending on the one whose argument (is_country or is_currency)
    is having true value

    Args:
        is_country - if True, indicates that countries
        api should be called

        is_currency - if True, indicates that exchange
        rate api should be called
    
    Returns:
        the json data of the requested api
    '''

    if (
        'is_country' not in kwargs.keys() and \
        'is_currency' not in kwargs.keys()
    ) or (
        'is_country' in kwargs.keys() and \
        'is_currency' in kwargs.keys()
    ):
        return None
    
    cache_ttl = int(getenv('CACHE_TTL'))
    if kwargs.get('is_country') :
        cache_key = getenv('COUNTRY_CACHE_KEY')
        external_api = getenv('COUNTRY_API')
    elif kwargs.get('is_currency'):
        cache_key = getenv('EXCHANGE_RATE_CACHE_KEY')
        external_api = getenv('CURRENCY_API')
    
    data = cache.get(cache_key)

    if data is None:
        # send request to the api
        data = requests.get(
            external_api,
            timeout=12
        ).json()
        # cache the obtained data
        cache.set(
            cache_key,
            data,
            cache_ttl
        )

    return data.get('rates') if kwargs.get('is_currency') else data


def parse_countries(countries):
    '''
    processes the countries by mapping the relevant elements are to
    expected keys and remove elements that are not needed

    Args:
        countries - the list of countries to be parsed

    Returns:
        the processed or parsed list
    '''
    countries_data = []

    for data in countries:
        # check if name or population or currencies are missing and raise exception for each
        # this has to be carried by the serializer since it is related to validation
        # if int(data.get('population')) < 1:
            # print('a missing population country is : ', data)

        currencies = data.pop('currencies', [])
        flag = data.pop('flag', '')
        data.pop('independent')

        if len(currencies) < 1:
            data['currency_code'] = None
            data['exchange_rate'] = None
            data['estimated_gdp'] = 0.0  # this is not needed since there is a default value specified by the model
        else:
            currencies_rate = get_countries_or_currency(
                is_currency=True
            )
            currency_code = currencies[0].get('code')
            exchange_rate = currencies_rate.get(currency_code, None)

            data['currency_code'] = currency_code
            data['exchange_rate'] = exchange_rate
            data['estimated_gdp'] = get_estimated_gdp(
                data.get('population'),
                exchange_rate
            ) if exchange_rate is not None else None
        data['flag_url'] = flag

        countries_data.append(data)

    # print(f'countries_data : {countries_data}')

    return countries_data


def get_estimated_gdp(population, exch_rate):
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


    


