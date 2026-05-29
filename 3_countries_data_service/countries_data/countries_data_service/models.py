from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator


class Country(models.Model):
    '''
    country resource model
    '''

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(max_length=250, unique=True)
    capital = models.CharField(max_length=250, blank=True)
    region = models.CharField(max_length=250, blank=True)
    population = models.IntegerField(validators=[MinValueValidator(0)])
    currency_code = models.CharField(max_length=3, null=True, default=None)
    exchange_rate = models.FloatField(null=True, default=None)
    estimated_gdp = models.FloatField(null=True, default=0.0)
    flag_url = models.URLField(blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["currency_code"]),
            models.Index(fields=["estimated_gdp"]),
            models.Index(fields=["-estimated_gdp"]),
            models.Index(fields=[
                "region", "currency_code", "estimated_gdp"
            ]),
            models.Index(fields=[
                "region", "currency_code", "-estimated_gdp"
            ]),
        ]
