from django.urls import path
from .views import (
    StringAnalysisListCreateView,
    StringAnalysisRetrieveDeleteView,
    StringAnalysisListView
)

urlpatterns = [
    path(
        'strings/',
        StringAnalysisListCreateView.as_view(),
        name='string-list-and-create-view'
    ),
    path(
        'strings/filter-by-natural-language/',
        StringAnalysisListView.as_view(),
        name='string-retrieve-view'
    ),
    path(
        'strings/<str:string_value>/',
        StringAnalysisRetrieveDeleteView.as_view(),
        name='string-retrieve-and-delete-view'
    ),
]

