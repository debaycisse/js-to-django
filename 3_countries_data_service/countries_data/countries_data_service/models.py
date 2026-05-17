from django.db import models
from uuid import uuid4

# Create your models here.

class Country(models.Model):
    # Model for a country instance

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    name = models.CharField(max_length=250)
    capital = models.CharField(max_length=250, blank=True)
    region = models.CharField(max_length=250, blank=True)
    population = models.IntegerField()
    currency_code = models.CharField(max_length=3, null=True)
    exchange_rate = models.FloatField(null=True)
    estimated_gdp = models.FloatField(default=0.0, null=True)
    flag_url = models.URLField(blank=True)
    last_refreshed_at = models.DateTimeField(auto_now=True)

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
