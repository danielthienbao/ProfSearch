from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_professor, name='search_professor'),
]
