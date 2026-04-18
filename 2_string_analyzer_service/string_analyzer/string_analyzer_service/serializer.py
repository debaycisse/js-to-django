from rest_framework import serializers
from .models import StringAnalysisModel


class StringAnalysisSerializer(serializers.ModelSerializer):
    '''
    Serilizer for String Analysis Model
    '''

    class Meta:
        model = StringAnalysisModel
        fields = ['id', 'value', 'created_at', 'properties']
