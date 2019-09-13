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
discover = config('discover')
discover_sort = config('discover_sort')
trending = config('trending')
discover_tv = config('discover_tv')


# Homepage view
def home_view(request):
    response = requests.get(trending + api_key)
    # store parsed json response for all trending shows and movies
    trending_all = response.json()
    trending = trending_all['results']
    return render(request, 'home.html', {'trending': trending})


# view for available movies
def available_movies(request):
    response = requests.get(discover + api_key + discover_sort)
    movies = response.json()
    movies = movies['results']
    return render(request, 'all_shows/movies.html', {'movies': movies})


# View to show available shows
def available_shows(request):
    response = requests.get(discover_tv + api_key + '&sort_by=popularity.desc')
    tv_shows = response.json()
    shows = tv_shows['results']
    return render(request, 'all_shows/tv_shows.html', {'shows': shows})


# View movie trailers via Youtube API
def view_trailers(request, id):
    movie = tmdb.Movies(id)  # Search for movie movie Id via tmdbsimple wrapper
    response = movie.info()

    youtube_instance = build(serviceName=yt_service_name,
                             version=yt_api_version,
                             developerKey=yt_api_key
                             )
    movie_name = movie.title
    search_response = youtube_instance.search().list(q=movie_name,
                                                     part='id, snippet',
                                                     maxResults=1).execute()
    for result in search_response.get('items', []):
        if result['id']['kind'] == 'youtube#video':
            video_id = result['id']['videoId']
    return render(request, 'focus.html', {'movie': movie, 'videoId': video_id})


# Create a movie search view
def search_movie(request):
    search_query = request.GET.get('search')
    search = tmdb.Search()
    response = search.movie(query=search_query)
    results = search.results
    return render(request, 'search.html', {
                                           'results': results,
                                           'query': search_query}
                  )
