"""
Enhanced features for the movie recommendation system:
- NLP Interface for natural language queries
- Movie similarity discovery
- Watchlist management
- Data visualizations
- Trending movies
- Movie comparisons
"""
import re
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Tuple, Optional
from textblob import TextBlob
import numpy as np
from collections import Counter
import requests
import json


class OpenRouterClient:
    """Client for OpenRouter API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "tngtech/deepseek-r1t2-chimera:free"
    
    def query(self, prompt: str, system_prompt: str = "") -> str:
        """Send a query to OpenRouter API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/AKolenda/Ai-for-business-assignment-3",
                "X-Title": "Movie Recommendation System"
            }
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            data = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            return f"Error querying OpenRouter API: {str(e)}"


class NLPInterface:
    """Natural language interface for movie queries"""
    
    @staticmethod
    def parse_query(query: str) -> Dict:
        """Parse natural language query into search parameters"""
        query_lower = query.lower()
        params = {}
        
        # Extract year
        year_match = re.search(r'\b(19|20)\d{2}\b', query)
        if year_match:
            params['year'] = int(year_match.group())
        
        # Extract decade
        decade_patterns = [
            (r'\b(nineteen )?(eighties|80s)\b', 1980),
            (r'\b(nineteen )?(nineties|90s)\b', 1990),
            (r'\b(two thousand|2000s)\b', 2000),
            (r'\b(twenty tens|2010s)\b', 2010),
            (r'\b(twenty twenties|2020s)\b', 2020),
        ]
        for pattern, decade in decade_patterns:
            if re.search(pattern, query_lower):
                params['decade'] = decade
                break
        
        # Extract genres
        genre_keywords = {
            'action': ['action', 'fight', 'battle'],
            'comedy': ['comedy', 'funny', 'humor', 'laugh'],
            'drama': ['drama', 'dramatic'],
            'horror': ['horror', 'scary', 'terrifying'],
            'thriller': ['thriller', 'suspense', 'suspenseful'],
            'romance': ['romance', 'romantic', 'love story'],
            'sci-fi': ['sci-fi', 'science fiction', 'scifi'],
            'fantasy': ['fantasy', 'magical'],
            'animation': ['animation', 'animated', 'cartoon'],
            'documentary': ['documentary', 'documentary'],
        }
        
        detected_genres = []
        for genre, keywords in genre_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected_genres.append(genre)
        
        if detected_genres:
            params['genres'] = detected_genres
        
        # Extract rating expectations
        if any(word in query_lower for word in ['highly rated', 'top rated', 'best', 'excellent']):
            params['min_rating'] = 7.0
        elif any(word in query_lower for word in ['good', 'quality']):
            params['min_rating'] = 6.0
        
        # Extract mood/sentiment
        blob = TextBlob(query)
        sentiment = blob.sentiment.polarity
        params['query_sentiment'] = sentiment
        
        # Extract popularity
        if any(word in query_lower for word in ['popular', 'trending', 'famous']):
            params['sort_by'] = 'popularity'
        
        # Extract title keywords (words not matching other patterns)
        stop_words = {'movie', 'movies', 'film', 'films', 'show', 'like', 'similar', 'about', 
                     'find', 'recommend', 'want', 'looking', 'for', 'with', 'from', 'the', 'a', 'an'}
        words = query_lower.split()
        title_keywords = [w for w in words if w not in stop_words and len(w) > 2]
        if title_keywords:
            params['keywords'] = ' '.join(title_keywords[:3])
        
        return params
    
    @staticmethod
    def generate_response(movies: List[Dict], query: str) -> str:
        """Generate natural language response for recommendations"""
        if not movies:
            return "I couldn't find any movies matching your criteria. Try adjusting your search!"
        
        count = len(movies)
        params = NLPInterface.parse_query(query)
        
        response_parts = [f"I found {count} movie{'s' if count != 1 else ''} for you"]
        
        if 'genres' in params:
            response_parts.append(f"in the {', '.join(params['genres'])} genre(s)")
        
        if 'year' in params:
            response_parts.append(f"from {params['year']}")
        elif 'decade' in params:
            response_parts.append(f"from the {params['decade']}s")
        
        if 'min_rating' in params:
            response_parts.append(f"with rating above {params['min_rating']}")
        
        return ' '.join(response_parts) + "!"


class WatchlistManager:
    """Manage personal movie watchlist"""
    
    def __init__(self):
        self.watchlist = []
        self.watched = []
        self.ratings = {}
    
    def add_to_watchlist(self, movie: Dict):
        """Add movie to watchlist"""
        movie_id = movie.get('id')
        if movie_id not in [m.get('id') for m in self.watchlist]:
            self.watchlist.append(movie)
            return True
        return False
    
    def remove_from_watchlist(self, movie_id: int):
        """Remove movie from watchlist"""
        self.watchlist = [m for m in self.watchlist if m.get('id') != movie_id]
    
    def mark_as_watched(self, movie_id: int, rating: Optional[float] = None):
        """Mark movie as watched"""
        movie = next((m for m in self.watchlist if m.get('id') == movie_id), None)
        if movie:
            self.watched.append(movie)
            self.remove_from_watchlist(movie_id)
            if rating:
                self.ratings[movie.get('title')] = rating
    
    def get_watchlist(self) -> List[Dict]:
        """Get current watchlist"""
        return self.watchlist
    
    def get_watched(self) -> List[Dict]:
        """Get watched movies"""
        return self.watched
    
    def get_ratings(self) -> Dict[str, float]:
        """Get user ratings"""
        return self.ratings


class MovieVisualizations:
    """Create data visualizations for movies"""
    
    @staticmethod
    def create_rating_distribution(movies: List[Dict]) -> go.Figure:
        """Create rating distribution histogram"""
        ratings = [m.get('vote_average', 0) for m in movies if m.get('vote_average')]
        
        fig = px.histogram(
            x=ratings,
            nbins=20,
            title="Movie Rating Distribution",
            labels={'x': 'Rating', 'y': 'Number of Movies'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(showlegend=False)
        return fig
    
    @staticmethod
    def create_genre_distribution(movies: List[Dict]) -> go.Figure:
        """Create genre distribution pie chart"""
        genre_counts = Counter()
        
        for movie in movies:
            genres = movie.get('genres', [])
            if isinstance(genres, list):
                for genre in genres:
                    if isinstance(genre, dict):
                        genre_counts[genre['name']] += 1
                    else:
                        genre_counts[str(genre)] += 1
        
        if not genre_counts:
            # Empty figure
            return go.Figure()
        
        labels = list(genre_counts.keys())
        values = list(genre_counts.values())
        
        fig = px.pie(
            names=labels,
            values=values,
            title="Genre Distribution"
        )
        return fig
    
    @staticmethod
    def create_timeline(movies: List[Dict]) -> go.Figure:
        """Create timeline of movies by release year"""
        years = []
        titles = []
        ratings = []
        
        for movie in movies:
            release_date = movie.get('release_date', '')
            if release_date:
                try:
                    year = int(release_date.split('-')[0])
                    years.append(year)
                    titles.append(movie.get('title', 'Unknown'))
                    ratings.append(movie.get('vote_average', 0))
                except (ValueError, IndexError):
                    continue
        
        if not years:
            return go.Figure()
        
        fig = px.scatter(
            x=years,
            y=ratings,
            hover_name=titles,
            title="Movies Timeline",
            labels={'x': 'Release Year', 'y': 'Rating'},
            color=ratings,
            color_continuous_scale='Viridis'
        )
        return fig
    
    @staticmethod
    def create_comparison_chart(movies: List[Dict]) -> go.Figure:
        """Create comparison chart for multiple movies"""
        if not movies:
            return go.Figure()
        
        titles = [m.get('title', 'Unknown')[:20] for m in movies[:10]]
        ratings = [m.get('vote_average', 0) for m in movies[:10]]
        popularity = [m.get('popularity', 0) for m in movies[:10]]
        vote_counts = [m.get('vote_count', 0) for m in movies[:10]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Rating (×10)',
            x=titles,
            y=[r * 10 for r in ratings],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Popularity',
            x=titles,
            y=popularity,
            marker_color='coral'
        ))
        
        fig.update_layout(
            title="Movie Comparison",
            xaxis_title="Movie",
            yaxis_title="Score",
            barmode='group',
            xaxis_tickangle=-45
        )
        
        return fig
    
    @staticmethod
    def create_top_actors_chart(movies: List[Dict], top_n: int = 10) -> go.Figure:
        """Create chart of most frequent actors with movie appearances"""
        actor_counts = Counter()
        actor_movies = {}  # Track which movies each actor appears in
        
        for movie in movies:
            movie_title = movie.get('title', 'Unknown')
            if 'credits' in movie and movie['credits']:
                cast = movie['credits'].get('cast', [])[:5]  # Top 5 actors per movie
                for actor in cast:
                    actor_name = actor['name']
                    actor_counts[actor_name] += 1
                    if actor_name not in actor_movies:
                        actor_movies[actor_name] = []
                    actor_movies[actor_name].append(movie_title)
            elif 'cast' in movie and movie['cast']:
                for actor in movie['cast'][:5]:
                    if isinstance(actor, dict):
                        actor_name = actor.get('name', 'Unknown')
                        actor_counts[actor_name] += 1
                        if actor_name not in actor_movies:
                            actor_movies[actor_name] = []
                        actor_movies[actor_name].append(movie_title)
        
        if not actor_counts:
            fig = go.Figure()
            fig.add_annotation(
                text="No actor data available in the current dataset",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14)
            )
            return fig
        
        top_actors = actor_counts.most_common(top_n)
        names = [actor for actor, _ in top_actors]
        counts = [count for _, count in top_actors]
        
        # Create hover text with movie titles
        hover_texts = []
        for actor, count in top_actors:
            movies_list = actor_movies[actor][:5]  # Show up to 5 movies
            more_text = f" (+{len(actor_movies[actor]) - 5} more)" if len(actor_movies[actor]) > 5 else ""
            hover_text = f"<b>{actor}</b><br>Appearances: {count}<br><br>Movies:<br>• " + "<br>• ".join(movies_list) + more_text
            hover_texts.append(hover_text)
        
        fig = go.Figure(data=[
            go.Bar(
                x=counts,
                y=names,
                orientation='h',
                marker=dict(
                    color=counts,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Appearances")
                ),
                text=counts,
                textposition='outside',
                hovertemplate='%{customdata}<extra></extra>',
                customdata=hover_texts
            )
        ])
        
        fig.update_layout(
            title=f"Top {top_n} Most Frequent Actors in Dataset<br><sub>Hover over bars to see movie titles</sub>",
            xaxis_title="Number of Movie Appearances",
            yaxis_title="Actor Name",
            yaxis={'categoryorder': 'total ascending'},
            height=max(400, top_n * 40),  # Dynamic height based on number of actors
            hovermode='closest'
        )
        
        return fig


class MovieComparison:
    """Compare multiple movies"""
    
    @staticmethod
    def compare_movies(movies: List[Dict]) -> pd.DataFrame:
        """Create comparison DataFrame for movies"""
        comparison_data = []
        
        for movie in movies:
            data = {
                'Title': movie.get('title', 'Unknown'),
                'Year': movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A',
                'Rating': movie.get('vote_average', 0),
                'Votes': movie.get('vote_count', 0),
                'Popularity': round(movie.get('popularity', 0), 1),
                'Runtime': f"{movie.get('runtime', 'N/A')} min" if movie.get('runtime') else 'N/A',
            }
            
            # Get genres
            genres = movie.get('genres', [])
            if isinstance(genres, list) and genres:
                if isinstance(genres[0], dict):
                    data['Genres'] = ', '.join([g['name'] for g in genres[:3]])
                else:
                    data['Genres'] = ', '.join([str(g) for g in genres[:3]])
            else:
                data['Genres'] = 'N/A'
            
            comparison_data.append(data)
        
        return pd.DataFrame(comparison_data)
    
    @staticmethod
    def get_similarities(movie1: Dict, movie2: Dict) -> Dict[str, any]:
        """Find similarities between two movies"""
        similarities = {
            'shared_genres': [],
            'shared_cast': [],
            'rating_difference': 0,
            'year_difference': 0
        }
        
        # Compare genres
        genres1 = set()
        genres2 = set()
        
        for genre in movie1.get('genres', []):
            if isinstance(genre, dict):
                genres1.add(genre['name'])
        
        for genre in movie2.get('genres', []):
            if isinstance(genre, dict):
                genres2.add(genre['name'])
        
        similarities['shared_genres'] = list(genres1.intersection(genres2))
        
        # Compare ratings
        similarities['rating_difference'] = abs(
            movie1.get('vote_average', 0) - movie2.get('vote_average', 0)
        )
        
        # Compare years
        year1 = movie1.get('release_date', '')[:4]
        year2 = movie2.get('release_date', '')[:4]
        if year1 and year2:
            try:
                similarities['year_difference'] = abs(int(year1) - int(year2))
            except ValueError:
                pass
        
        return similarities
