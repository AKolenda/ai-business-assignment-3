"""
TMDB API Client for fetching movie metadata
"""
import requests
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import time

load_dotenv()


class TMDBClient:
    """Client for interacting with The Movie Database (TMDB) API"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize TMDB client with API key"""
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        if not self.api_key:
            raise ValueError("TMDB API key not found. Set TMDB_API_KEY environment variable.")
        self.session = requests.Session()
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to TMDB API with rate limiting"""
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {e}")
            return {}
    
    def search_movies(self, query: str, page: int = 1) -> Dict:
        """Search for movies by title"""
        return self._make_request("search/movie", {
            "query": query,
            "page": page,
            "include_adult": False
        })
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a movie"""
        return self._make_request(f"movie/{movie_id}", {
            "append_to_response": "credits,keywords,reviews,similar,recommendations"
        })
    
    def get_popular_movies(self, page: int = 1) -> Dict:
        """Get popular movies"""
        return self._make_request("movie/popular", {"page": page})
    
    def get_top_rated_movies(self, page: int = 1) -> Dict:
        """Get top rated movies"""
        return self._make_request("movie/top_rated", {"page": page})
    
    def get_trending_movies(self, time_window: str = "week") -> Dict:
        """Get trending movies (day or week)"""
        return self._make_request(f"trending/movie/{time_window}")
    
    def get_now_playing(self, page: int = 1) -> Dict:
        """Get movies currently in theaters"""
        return self._make_request("movie/now_playing", {"page": page})
    
    def get_upcoming_movies(self, page: int = 1) -> Dict:
        """Get upcoming movies"""
        return self._make_request("movie/upcoming", {"page": page})
    
    def discover_movies(self, **kwargs) -> Dict:
        """
        Discover movies with various filters
        
        Supported parameters:
        - with_genres: Genre IDs separated by comma
        - primary_release_year: Year
        - vote_average.gte: Minimum rating
        - vote_average.lte: Maximum rating
        - with_runtime.gte: Minimum runtime
        - with_runtime.lte: Maximum runtime
        - with_cast: Actor IDs
        - with_crew: Crew member IDs
        - sort_by: Sort order (popularity.desc, vote_average.desc, etc.)
        """
        return self._make_request("discover/movie", kwargs)
    
    def get_genres(self) -> Dict:
        """Get list of movie genres"""
        return self._make_request("genre/movie/list")
    
    def search_person(self, query: str, page: int = 1) -> Dict:
        """Search for people (actors, directors, etc.)"""
        return self._make_request("search/person", {
            "query": query,
            "page": page
        })
    
    def get_person_details(self, person_id: int) -> Dict:
        """Get detailed information about a person"""
        return self._make_request(f"person/{person_id}", {
            "append_to_response": "movie_credits"
        })
    
    def get_movie_reviews(self, movie_id: int) -> Dict:
        """Get reviews for a movie"""
        return self._make_request(f"movie/{movie_id}/reviews")
