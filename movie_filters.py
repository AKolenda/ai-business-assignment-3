"""
Movie filtering utilities for temporal, quality, content, personnel, and genre filters
"""
from typing import List, Dict, Optional
import pandas as pd


class MovieFilters:
    """Comprehensive movie filtering system"""
    
    @staticmethod
    def filter_by_year(
        movies: List[Dict], 
        min_year: Optional[int] = None,
        max_year: Optional[int] = None
    ) -> List[Dict]:
        """Filter movies by release year"""
        filtered = []
        for movie in movies:
            release_date = movie.get('release_date', '')
            if release_date:
                try:
                    year = int(release_date.split('-')[0])
                    if min_year and year < min_year:
                        continue
                    if max_year and year > max_year:
                        continue
                    filtered.append(movie)
                except (ValueError, IndexError):
                    continue
        return filtered
    
    @staticmethod
    def filter_by_decade(movies: List[Dict], decade: int) -> List[Dict]:
        """Filter movies by decade (e.g., 1990, 2000, 2010)"""
        return MovieFilters.filter_by_year(
            movies, 
            min_year=decade, 
            max_year=decade + 9
        )
    
    @staticmethod
    def filter_by_rating(
        movies: List[Dict],
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None
    ) -> List[Dict]:
        """Filter movies by vote average (quality filter)"""
        filtered = []
        for movie in movies:
            rating = movie.get('vote_average', 0)
            if min_rating and rating < min_rating:
                continue
            if max_rating and rating > max_rating:
                continue
            filtered.append(movie)
        return filtered
    
    @staticmethod
    def filter_by_vote_count(
        movies: List[Dict],
        min_votes: Optional[int] = None
    ) -> List[Dict]:
        """Filter movies by minimum vote count (quality filter)"""
        filtered = []
        for movie in movies:
            votes = movie.get('vote_count', 0)
            if min_votes and votes < min_votes:
                continue
            filtered.append(movie)
        return filtered
    
    @staticmethod
    def filter_by_runtime(
        movies: List[Dict],
        min_runtime: Optional[int] = None,
        max_runtime: Optional[int] = None
    ) -> List[Dict]:
        """Filter movies by runtime in minutes (content specification)"""
        filtered = []
        for movie in movies:
            runtime = movie.get('runtime', 0)
            if runtime == 0:  # Skip movies without runtime data
                continue
            if min_runtime and runtime < min_runtime:
                continue
            if max_runtime and runtime > max_runtime:
                continue
            filtered.append(movie)
        return filtered
    
    @staticmethod
    def filter_by_language(
        movies: List[Dict],
        languages: List[str]
    ) -> List[Dict]:
        """Filter movies by original language (content specification)"""
        if not languages:
            return movies
        
        filtered = []
        for movie in movies:
            lang = movie.get('original_language', '')
            if lang in languages:
                filtered.append(movie)
        return filtered
    
    @staticmethod
    def filter_by_genres(
        movies: List[Dict],
        genre_ids: List[int] = None,
        genre_names: List[str] = None
    ) -> List[Dict]:
        """Filter movies by genres"""
        if not genre_ids and not genre_names:
            return movies
        
        filtered = []
        for movie in movies:
            movie_genres = movie.get('genres', [])
            if not movie_genres:
                movie_genres = movie.get('genre_ids', [])
            
            # Check genre IDs
            if genre_ids:
                if isinstance(movie_genres, list):
                    if isinstance(movie_genres[0], dict):
                        movie_genre_ids = [g['id'] for g in movie_genres]
                    else:
                        movie_genre_ids = movie_genres
                    
                    if any(gid in movie_genre_ids for gid in genre_ids):
                        filtered.append(movie)
                        continue
            
            # Check genre names
            if genre_names:
                if isinstance(movie_genres, list) and movie_genres:
                    if isinstance(movie_genres[0], dict):
                        movie_genre_names = [g['name'].lower() for g in movie_genres]
                        if any(name.lower() in movie_genre_names for name in genre_names):
                            filtered.append(movie)
        
        return filtered
    
    @staticmethod
    def filter_by_cast(
        movies: List[Dict],
        actor_names: List[str]
    ) -> List[Dict]:
        """Filter movies by cast members (personnel filter)"""
        if not actor_names:
            return movies
        
        filtered = []
        actor_names_lower = [name.lower() for name in actor_names]
        
        for movie in movies:
            # Check credits
            if 'credits' in movie and movie['credits']:
                cast = movie['credits'].get('cast', [])
                for actor in cast:
                    if actor['name'].lower() in actor_names_lower:
                        filtered.append(movie)
                        break
            # Check direct cast field
            elif 'cast' in movie and movie['cast']:
                for actor in movie['cast']:
                    actor_name = actor.get('name', '') if isinstance(actor, dict) else str(actor)
                    if actor_name.lower() in actor_names_lower:
                        filtered.append(movie)
                        break
        
        return filtered
    
    @staticmethod
    def filter_by_director(
        movies: List[Dict],
        director_name: str
    ) -> List[Dict]:
        """Filter movies by director (personnel filter)"""
        if not director_name:
            return movies
        
        filtered = []
        director_name_lower = director_name.lower()
        
        for movie in movies:
            # Check credits
            if 'credits' in movie and movie['credits']:
                crew = movie['credits'].get('crew', [])
                for person in crew:
                    if (person.get('job') == 'Director' and 
                        person['name'].lower() == director_name_lower):
                        filtered.append(movie)
                        break
            # Check direct director field
            elif 'director' in movie:
                if movie['director'].lower() == director_name_lower:
                    filtered.append(movie)
        
        return filtered
    
    @staticmethod
    def filter_by_popularity(
        movies: List[Dict],
        min_popularity: Optional[float] = None
    ) -> List[Dict]:
        """Filter movies by popularity score"""
        if not min_popularity:
            return movies
        
        filtered = []
        for movie in movies:
            popularity = movie.get('popularity', 0)
            if popularity >= min_popularity:
                filtered.append(movie)
        return filtered
    
    @staticmethod
    def apply_filters(
        movies: List[Dict],
        filters: Dict
    ) -> List[Dict]:
        """Apply multiple filters at once"""
        filtered_movies = movies
        
        # Temporal filters
        if 'min_year' in filters or 'max_year' in filters:
            filtered_movies = MovieFilters.filter_by_year(
                filtered_movies,
                filters.get('min_year'),
                filters.get('max_year')
            )
        
        if 'decade' in filters:
            filtered_movies = MovieFilters.filter_by_decade(
                filtered_movies,
                filters['decade']
            )
        
        # Quality filters
        if 'min_rating' in filters or 'max_rating' in filters:
            filtered_movies = MovieFilters.filter_by_rating(
                filtered_movies,
                filters.get('min_rating'),
                filters.get('max_rating')
            )
        
        if 'min_votes' in filters:
            filtered_movies = MovieFilters.filter_by_vote_count(
                filtered_movies,
                filters['min_votes']
            )
        
        # Content specifications
        if 'min_runtime' in filters or 'max_runtime' in filters:
            filtered_movies = MovieFilters.filter_by_runtime(
                filtered_movies,
                filters.get('min_runtime'),
                filters.get('max_runtime')
            )
        
        if 'languages' in filters:
            filtered_movies = MovieFilters.filter_by_language(
                filtered_movies,
                filters['languages']
            )
        
        # Genre filters
        if 'genre_ids' in filters or 'genre_names' in filters:
            filtered_movies = MovieFilters.filter_by_genres(
                filtered_movies,
                filters.get('genre_ids'),
                filters.get('genre_names')
            )
        
        # Personnel filters
        if 'actors' in filters:
            filtered_movies = MovieFilters.filter_by_cast(
                filtered_movies,
                filters['actors']
            )
        
        if 'director' in filters:
            filtered_movies = MovieFilters.filter_by_director(
                filtered_movies,
                filters['director']
            )
        
        # Popularity filter
        if 'min_popularity' in filters:
            filtered_movies = MovieFilters.filter_by_popularity(
                filtered_movies,
                filters['min_popularity']
            )
        
        return filtered_movies
