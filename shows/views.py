import json
from django.shortcuts import render
import requests
from decouple import config
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import tmdbsimple as tmdb

api_key = config('MD_KEY')
yt_api_key = config('YT_API_KEY')
yt_service_name = config('YT_SERVICE_NAME')
yt_api_version = config('YT_API_VERSION')
tmdb.API_KEY = config('MD_KEY')

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

# View movie trailers via Youtube API
def view_trailers(request, id):
    movie = tmdb.Movies(id) # Search for movie using movie Id via tmdbsimple wrapper
    response = movie.info()

    youtube_instance = build(serviceName=yt_service_name, version=yt_api_version, developerKey=yt_api_key)
    movie_name = movie.title
    search_response = youtube_instance.search().list(q=movie_name, part='id, snippet', maxResults=1).execute()
    for result in search_response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            video_id = result['id']['videoId']
    return render(request, 'focus.html', {'movie': movie, 'videoId': video_id})

def search_movie(request):
    search_query = request.GET.get('search')
    search = tmdb.Search()
    response = search.movie(query=search_query)
    results = search.results
    
    return render( request, 'search.html', {'results':results, 'query':search_query})
