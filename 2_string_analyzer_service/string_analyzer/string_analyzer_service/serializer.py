from rest_framework import serializers
from .models import StringAnalysisModel
from . import custom_http_exceptions as che


class StringAnalysisSerializer(serializers.Serializer):
    '''
    Serilizer for String Analysis Model
    '''
    id = serializers.CharField(read_only=True)
    value = serializers.CharField(
        required=True, allow_blank=True, allow_null=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    properties = serializers.JSONField(read_only=True)
    
    def validate_value(self, value):
        '''
        Handles the validation of the "value" field

        Args:
            self - instance of this serializer class
            value - the passed value of the "value" field
        '''

        if not isinstance(value, str):
            raise che.UnprocessableEntity422()
        
        if len(value) < 1:
            raise che.BadRequest400()

        if StringAnalysisModel.objects.filter(value=value).exists():
            raise che.Conflict409()
        
        return value

    def create(self, validated_data):
        '''
        Handles the creation of an instance of this serializer.

        Args:
            self - an instance of this serializer class
            validated_data - validated dictionary of
            the passed POST request data 
        '''
        model_instance = StringAnalysisModel\
            .objects.create(**validated_data)
        
        return model_instance

    def to_representation(self, instance):
        '''
        Handles instance representation and handles the formatting
        for the created_at datetime field here

        Args:
            self - an instance of this serializer class
            instance - a retrieved instance
        '''
        instance_data = super().to_representation(instance=instance)

        if instance_data['created_at']:
            instance_data['created_at'] =\
                instance_data['created_at'][:-4] + 'Z'
        return instance_data
