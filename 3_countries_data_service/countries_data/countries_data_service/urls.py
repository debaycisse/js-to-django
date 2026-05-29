from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSets, CountryStatusViewSets


router = DefaultRouter(trailing_slash=False)

router.register(
    r'countries',
    CountryViewSets,
    basename='countries-view'
)

router.register(
    r'',
    CountryStatusViewSets,
    basename='countries-status-view'
)

urlpatterns = [
    path('', include(router.urls)),
]
