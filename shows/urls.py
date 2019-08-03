from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('movies/', views.available_movies, name='movies'),
    path('shows/', views.available_shows, name='shows')
]