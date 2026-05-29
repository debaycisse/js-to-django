from os import path
import requests
from urllib.parse import urlparse
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, serializers
from rest_framework.decorators import action
from .models import Country
from .serializers import CountrySerializer
from .utilities import get_countries_or_currency, parse_countries
from .image_utils import (
    generate_image,
    get_last_refreshed_at,
    get_country_counts
)


class CountryViewSets(viewsets.GenericViewSet):

    '''
    Country view sets contains all the view handlers
    for the countries resource
    '''

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = 'name'

    def list(self, request, format=None):
        '''
        handles the GET request that's sent to /countries with
        its filtering and sorting keywords
        '''
        region = request.query_params.get('region')
        currency = request.query_params.get('currency')
        sort_value = request.query_params.get('sort')
        order_value = 'name'

        if sort_value == 'gdp_desc':
            order_value = '-estimated_gdp'
        elif sort_value == 'gdp_asc':
            order_value = 'estimated_gdp'

        countries_qs = self.get_queryset()

        if region:
            countries_qs = self.get_queryset().filter(region=region)
        
        if currency:
            countries_qs = countries_qs.filter(currency_code=currency)

        countries_qs = countries_qs.order_by(order_value)

        serializer = self.get_serializer(countries_qs, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, name=None, format=None):
        '''
        handles or processes a GET /countries/:name
        request by otaining a single country (resource) instance
        '''
        country = self.get_object()
        serializer = self.get_serializer(country)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, name=None, format=None):
        '''
        handles or processes the DELETE /countries/:name
        request by deleting a single country (resource) instance
        '''
        try:

            country = self.get_object()
            country.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Country.DoesNotExist:
            return Response(
                {'message': 'country not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(methods=['POST'], detail=False)
    def refresh(self, request, format=None):
        '''
        handles or processes the POST /countries/refresh
        request for updating existing countries and
        inserting new ones (upserting)
        '''
        try:
            countries = get_countries_or_currency(is_country=True)
            countries = parse_countries(countries)

            serializer = self.get_serializer(data=countries, many=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
            
                # generate the image that contains country's status
                generate_image()

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

        except requests.exceptions.ConnectTimeout as e:
            api_name = urlparse(e.request.url).netloc
            return Response(
                {
                    'error': 'External data source unavailable',
                    'details': f'Could not fetch data from {api_name}'
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except serializers.ValidationError as e:
            return Response(
                {
                    'error': 'Validation failed',
                    'details': e.get_full_details()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['GET'], detail=False)
    def image(self, request, format=None):
        '''
        handles the request that's sent to GET /countries/image route and
        serves the url with which one can view an image that contains some
        statistics about the countries cache
        '''

        # construct the image's name and contained directory
        image_name = 'summary.png'
        dir_name = settings.MEDIA_ROOT
        image_path = path.join(dir_name, image_name)

        # Handle a missing file
        if not path.exists(image_path):
            return Response(
                {'error': 'Summary image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # contruct an absolute url path to the image
        image_url = request.build_absolute_uri(
            f'{settings.MEDIA_URL}{image_name}'
        )

        return Response(
            { 'image': image_url },
            status=status.HTTP_200_OK
        )

class CountryStatusViewSets(viewsets.GenericViewSet):

    '''
    This view houses the implementation of the /status
    view handler which handles the status of the countries
    '''
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    @action(methods=['GET'], detail=False)
    def status(self, request, format=None):
        '''
        handles the GET request that's sent to /status route and
        returns the status of the countries cache
        '''

        total_countries = get_country_counts()
        last_refreshed_at = get_last_refreshed_at()

        return Response(
            {
                'total_countries': total_countries,
                'last_refreshed_at': last_refreshed_at,
            },
            status=status.HTTP_200_OK
        )
