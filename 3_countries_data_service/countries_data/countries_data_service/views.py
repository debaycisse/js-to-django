from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from .models import Country
from .serializers import CountrySerializer
from .utilities import get_countries_or_currency, generate_image



"""

[DONE]GET /countries
[DONE]GET /countries?region=Africa
[DONE]GET /countries?currency=NGN
[DONE]GET /countries?sort=gdp_desc
[DONE]GET /countries?region=Africa&currency=NGN&sort=gdp_desc

GET /countries/image
[DONE]POST /countries/refresh

[DONE]GET /countries/:name
[DONE]DELETE /countries/:name

GET /status

"""

class CountryViewSets(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):

    """
    CountryViewSets contains all the view handlers for the country
    """

    lookup_field = 'name'

    def list(self, request, format=None):
        '''
        handles the below GET request to /countries with
        its filtering and sorting
        
        :param self: the view instance or object
        :param request: http request object
        :param format: user prefered response format
        '''
        region = request.query_params.get('region')
        currency = request.query_params.get('currency')
        sort_value = request.query_params.get('sort')
        order_value = 'estimated_gdp'

        if sort_value == 'gdp_desc':
            order_value = '-estimated_gdp'

        queryset = Country\
            .objects\
            .filter(region=region, currency_code=currency)\
            .order_by(order_value)
        
        serializer = CountrySerializer(queryset, many=True)
        
        return Response(serializer.data)
    
    def retrieve(self, request, name=None, format=None):
        '''
        handles or processes a GET /countries/:name
        request for a single country (resource)
        
        :param self: the view's instance or object
        :param request: http request's object
        :param name: the url parameter that holds the country's name
        :param format: user's preferred view format
        '''
        country = Country.objects.get(name=name)
        serializer = CountrySerializer(country)

        return Response(serializer.data)
    
    def destroy(self, request, name=None, format=None):
        '''
        handles or processes the DELETE /countries/:name
        request for a signle country (resource)
        
        :param self: the view's instance or object
        :param request: http request's object
        :param name: the url parameter that holds the country's name
        :param format: user's preferred view format
        '''
        try:

            country = Country.objects.get(name=name)

            if country is not None:
                country.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Country.DoesNotExist:
            return Response(
                {'message': 'country not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(methods=['POST'], detail=False)
    def refresh(self, request, format=None):
        '''
        handles or processes the POST /countries/refresh
        request for upserting countries
        
        :param self: the view's instance or object
        :param request: http request's object
        :param format: user's preferred view format
        '''
        countries = get_countries_or_currency(is_country=True)
        serializer = CountrySerializer(countries, many=True)
        if serializer.is_valid():
            serializer.save()
        
        # generate the image
        generate_image()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
