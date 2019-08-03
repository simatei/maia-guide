import json
from django.shortcuts import render
import requests
from decouple import config

api_key = config('MD_KEY')

# Homepage view
def home_view(request):
    response = requests.get('https://api.themoviedb.org/3/trending/all/day?api_key=' +  api_key)
    trending_all = response.json() # store parsed json response for all trending shows and movies
    trending = trending_all['results']
    return render(request, 'home.html', {'trending':trending})

# view for available movies
def available_movies(request):
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=' +  api_key + '&primary_release_year=2019&sort_by=popularity.desc')
    movies = response.json() 
    movies = movies['results']
    return render(request, 'all_shows/movies.html', {'movies':movies})
    
def available_shows(request):
    response = requests.get('https://api.themoviedb.org/3/discover/tv?api_key=' +  api_key + '&sort_by=popularity.desc')
    tv_shows = response.json() 
    shows = tv_shows['results']
    return render(request,'all_shows/tv_shows.html', {'shows': shows})