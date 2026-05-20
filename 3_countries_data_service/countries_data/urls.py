from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(include('countries_data.countries_data_service.urls')),
    path('admin/', admin.site.urls),
]
