from django.db import models
from hashlib import sha256
from . import utils

# Create your models here.
class StringAnalysisModel(models.Model):
    '''
    The model for storing an instance of an analysed string
    '''
    id = models.CharField(
        primary_key=True,
        blank=True,
        serialize=True,
        editable=False,
        max_length=64,
    )
    value = models.CharField(editable=False)
    created_at = models.DateTimeField(
        default=utils.created_at, editable=False
    )
    properties = models.JSONField(blank=True)

    def save(self, *args, **kwargs):
        '''Updates properties before saving an instance'''
        str_obj = utils.StringProperties(self.value)
    
        if not self.id:
            self.id = str_obj.get_sha256()

        self.properties = {
            'length': str_obj.length,
            'is_palindrome': str_obj.is_palindrome(),
            'unique_characters': str_obj.get_unique_characters_count(),
            'word_count': str_obj.get_word_counts(),
            'sha256_hash': str_obj.get_sha256(),
            'character_frequency_map': str_obj.get_char_freq_map(),
        }
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'string_analysis_model'
