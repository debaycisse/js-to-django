from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .data import user


class View_me(APIView):
    def get(self, request, format=None):
        print('format : {}'.format(format))
        return Response(user.get_user_object())
