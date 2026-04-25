from rest_framework import generics, status
from .models import StringAnalysisModel
from .serializer import StringAnalysisSerializer
from rest_framework.response import Response
from .utils import (
    obtain_id, 
    validate_query_params, 
    get_filters, 
    validate_filters,
)
from . import custom_http_exceptions as che


class StringAnalysisListCreateView(generics.ListCreateAPIView):
    '''
    Handles requests for the following urls

    POST -> /strings
    GET -> /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a
    '''

    serializer_class = StringAnalysisSerializer

    def get_queryset(self):
        '''
        Controls how a query is performed using
        query parameters that are passed from an HTTP request.

        Args:
            self - an instance of ListCreateAPIView
        '''

        queryset = StringAnalysisModel.objects.all()
        query_params = self.request.query_params
        is_palindrome = query_params.get('is_palindrome')
        min_length = query_params.get('min_length')
        max_length = query_params.get('max_length')
        word_count = query_params.get('word_count')
        cnt_ch = query_params.get('contains_character')

        if is_palindrome is not None:
            validate_query_params(
                is_palindrome != 'true' and is_palindrome != 'false'
            )
            is_palindrome = False if is_palindrome == 'false' else True
            queryset = queryset.filter(
                properties__is_palindrome=is_palindrome)
        if min_length is not None:
            try:
                min_length = int(min_length)
                queryset = queryset.filter(
                    properties__length__gte=min_length)
            except (TypeError, ValueError):
                validate_query_params(True)
        if max_length is not None:
            try:
                max_length = int(max_length)
                queryset = queryset.filter(
                    properties__length__lte=max_length)
            except (TypeError, ValueError):
                validate_query_params(True)
        if word_count is not None:
            try:
                word_count = int(word_count)
                queryset = queryset.filter(
                    properties__word_count=word_count)
            except (TypeError, ValueError):
                validate_query_params(True)
        if cnt_ch is not None:
            validate_query_params(
                len(cnt_ch) > 1
            )
            queryset = queryset.filter(
                properties__character_frequency_map__has_key=cnt_ch)
        return queryset

    def get_paginated_response(self, data):
        '''
        Controls what data make up the response data for every
        HTTP request that is handled by this view.

        Args:
            self - an instance of this view
            data - the serialized queryset data
        '''

        filters_applied = {}
        query_params = self.request.query_params
        is_pal = query_params.get('is_palindrome')
        min_length = query_params.get('min_length')
        max_length = query_params.get('max_length')
        word_count = query_params.get('word_count')
        cont_ch = query_params.get('contains_character')

        if is_pal is not None:
            filters_applied['is_palindrome'] =\
                True if is_pal == 'true' else False
        if min_length is not None:
            filters_applied['min_length'] = int(min_length)
        if max_length is not None:
            filters_applied['max_length'] = int(max_length)
        if word_count is not None:
            filters_applied['word_count'] = int(word_count)
        if cont_ch is not None:
            filters_applied['contains_character'] = cont_ch

        return Response(
            {
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'count': self.paginator.page.paginator.count,
                'data': data,
                'filters_applied': filters_applied
            }
        )

class StringAnalysisRetrieveDeleteView(
    generics.RetrieveDestroyAPIView
    ):
    '''
    Handles requests for the following urls

    GET -> /strings/{string_value}
    DELETE -> /strings/{string_value}
    '''
    queryset = StringAnalysisModel.objects.all()
    serializer_class = StringAnalysisSerializer

    def get_object(self):
        '''
        Handles retriving of an object whose string's value is
        passed from the HTTP GET request

        Args:
            self - instance of this view (RetrieveDestroyAPIView) class
        '''
        string_value = self.kwargs.get('string_value')
        hash_value = obtain_id(string_value)

        try:
            return StringAnalysisModel.objects.get(id=hash_value)
        except StringAnalysisModel.DoesNotExist:
            raise che.NotFound404()

class StringAnalysisListView(generics.ListAPIView):
    '''
    Handles requests for the following url

    * GET /strings/filter-by-natural-language?query=all%20single%20word%20palindromic%20strings

    Example queries:
        - "all single word palindromic strings"
        - "strings longer than 10 characters"
        - "palindromic strings that contain the first vowel"
        - "strings containing the letter z"
    '''
    serializer_class = StringAnalysisSerializer

    def get_queryset(self):
        '''
        Acts in the absense of providing queryset
        attribute in this class

        Handles how objects or instances of the StringAnalysisModel
        are retrieved from the model
        '''
        query = self.request.query_params.get('query')

        validate_query_params(
            query is None,
            'Unable to parse natural language query'
        )

        validate_query_params(
            len(query) < 4,
            'Unable to parse natural language query'
        )

        filters = get_filters(query=query)

        validate_filters(len(filters.keys()) < 1)

        validate_filters(
            (
                filters.get('min_length') and \
                filters.get('max_length')
            ) and \
            (filters.get('min_length') > filters.get('max_length'))
        )

        validate_filters(
            filters.get('contains_character') and \
            (len(filters.get('contains_character')) > 1) 
        )

        queryset = StringAnalysisModel.objects.all()
        
        if filters is not None and len(filters.keys()) > 0:
            is_palindrome = filters.get('is_palindrome')
            min_length = filters.get('min_length')
            max_length = filters.get('max_length')
            word_count = filters.get('word_count')
            cnt_ch = filters.get('contains_character')
            if is_palindrome is not None:
                queryset = queryset.filter(
                    properties__is_palindrome=is_palindrome
                )
            if min_length is not None:
                queryset = queryset.filter(
                    properties__length__gte=int(min_length)
                )
            if max_length is not None:
                queryset = queryset.filter(
                    properties__length__lte=int(max_length)
                )
            if word_count is not None:
                queryset = queryset.filter(
                    properties__word_count=int(word_count)
                )
            if cnt_ch is not None:
                queryset = queryset.filter(
                    properties__character_frequency_map__has_key=cnt_ch
                )
        return queryset


    def get_paginated_response(self, data):
        '''
        Controls what data make up the response data for every HTTP
        request that is handled by this view.

        Args:
            self - an instance of this view
            data - the serialized queryset data
        '''

        query: str | None = self.request.query_params.get(
            'query'
        ) or None

        filters_keyword: dict | dict[str, str | None] = \
            get_filters(query=query)

        filters_applied: dict | dict[str, str | int | bool] = {}

        is_pal: bool | None = filters_keyword.get('is_palindrome')
        min_length: str | None = filters_keyword.get('min_length')
        max_length: str | None = filters_keyword.get('max_length')
        word_count: str | None = filters_keyword.get('word_count')
        cont_ch: str | None = filters_keyword.get('contains_character')

        if is_pal is not None:
            filters_applied['is_palindrome'] = is_pal
        if min_length is not None:
            filters_applied['min_length'] = int(min_length)
        if max_length is not None:
            filters_applied['max_length'] = int(max_length)
        if word_count is not None:
            filters_applied['word_count'] = int(word_count)
        if cont_ch is not None:
            filters_applied['contains_character'] = cont_ch

        return Response(
            {
                'next': self.paginator.get_next_link(),
                'previous': self.paginator.get_previous_link(),
                'count': self.paginator.page.paginator.count,
                'data': data,
                'filters_applied': filters_applied
            }
        )