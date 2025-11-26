"""
Movie Recommendation Engine with multiple approaches:
- Content-Based Filtering
- Sentiment-Based NLP
- Collaborative Filtering
- Hybrid Recommendations
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import nltk
from typing import List, Dict, Tuple
import re
from difflib import SequenceMatcher

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords


class RecommendationEngine:
    """Multi-approach recommendation engine for movies"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.tfidf_vectorizer = None
        self.tfidf_matrix = None
        self.movies_df = None
        
    def prepare_data(self, movies: List[Dict]):
        """Prepare movie data for recommendations"""
        if not movies:
            return
        
        # Convert to DataFrame
        self.movies_df = pd.DataFrame(movies)
        
        # Create combined feature for content-based filtering
        self.movies_df['combined_features'] = self.movies_df.apply(
            lambda x: self._combine_features(x), axis=1
        )
        
        # Create TF-IDF matrix
        self.tfidf_vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movies_df['combined_features']
        )
    
    def _combine_features(self, row: pd.Series) -> str:
        """Combine movie features into a single string for TF-IDF vectorization"""
        features = []
        
        # Add title (weighted by repetition for importance)
        if 'title' in row and pd.notna(row['title']):
            features.append(str(row['title']) * 3)
        
        # Add genres
        if 'genres' in row and row['genres']:
            if isinstance(row['genres'], list):
                for g in row['genres']:
                    if isinstance(g, dict):
                        features.append(g['name'])
                    else:
                        features.append(str(g))
            else:
                features.append(str(row['genres']))
        
        # Add overview
        if 'overview' in row and pd.notna(row['overview']):
            features.append(str(row['overview']))
        
        # Add keywords
        if 'keywords' in row and row['keywords']:
            if isinstance(row['keywords'], dict) and 'keywords' in row['keywords']:
                features.extend([k['name'] for k in row['keywords']['keywords']])
        
        # Add cast (top actors)
        if 'credits' in row and row['credits']:
            if isinstance(row['credits'], dict) and 'cast' in row['credits']:
                features.extend([actor['name'] for actor in row['credits']['cast'][:5]])
        elif 'cast' in row and row['cast']:
            if isinstance(row['cast'], list):
                for actor in row['cast'][:5]:
                    if isinstance(actor, dict):
                        features.append(actor.get('name', ''))
                    else:
                        features.append(str(actor))
        
        # Add director
        if 'credits' in row and row['credits']:
            if isinstance(row['credits'], dict) and 'crew' in row['credits']:
                for person in row['credits']['crew']:
                    if person.get('job') == 'Director':
                        features.append(person['name'])
                        break
        elif 'director' in row and row['director']:
            features.append(str(row['director']))
        
        return ' '.join(features).lower()
    
    def _normalize_title(self, title: str) -> str:
        """Normalize movie title for matching"""
        # Remove special characters and extra spaces
        normalized = re.sub(r'[^\w\s]', '', title.lower())
        normalized = ' '.join(normalized.split())
        return normalized
    
    def _find_best_match(self, title: str) -> Tuple[int, float]:
        """Find the best matching movie index using fuzzy matching"""
        if self.movies_df is None:
            return -1, 0.0
        
        normalized_input = self._normalize_title(title)
        best_idx = -1
        best_score = 0.0
        
        for idx, row in self.movies_df.iterrows():
            movie_title = row.get('title', '')
            if not movie_title:
                continue
            
            normalized_movie = self._normalize_title(movie_title)
            
            # Exact match (normalized)
            if normalized_input == normalized_movie:
                return idx, 1.0
            
            # Check if input is contained in movie title or vice versa
            if normalized_input in normalized_movie or normalized_movie in normalized_input:
                score = 0.9
                if score > best_score:
                    best_score = score
                    best_idx = idx
                continue
            
            # Fuzzy matching using SequenceMatcher
            score = SequenceMatcher(None, normalized_input, normalized_movie).ratio()
            if score > best_score:
                best_score = score
                best_idx = idx
        
        return best_idx, best_score
    
    def content_based_recommendations(
        self, 
        movie_title: str, 
        n_recommendations: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Content-based filtering recommendations with improved matching.
        Returns list of (movie_id, similarity_score) tuples.
        """
        if self.movies_df is None or self.tfidf_matrix is None:
            return []
        
        # Try exact match first (case-insensitive)
        exact_match = self.movies_df[
            self.movies_df['title'].str.lower() == movie_title.lower()
        ]
        
        if not exact_match.empty:
            idx = exact_match.index[0]
        else:
            # Try fuzzy matching
            idx, match_score = self._find_best_match(movie_title)
            if idx == -1 or match_score < 0.5:
                return []
        
        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(
            self.tfidf_matrix[idx:idx+1], 
            self.tfidf_matrix
        ).flatten()
        
        # Get top similar movies (excluding the input movie)
        similar_indices = cosine_similarities.argsort()[::-1][1:n_recommendations+1]
        
        recommendations = [
            (self.movies_df.iloc[i]['id'], cosine_similarities[i])
            for i in similar_indices
            if 'id' in self.movies_df.iloc[i]
        ]
        
        return recommendations
    
    def fuzzy_content_recommendations(
        self,
        movie_title: str,
        movies: List[Dict],
        n_recommendations: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Fallback fuzzy content-based recommendations when exact match fails.
        Searches by genre and keyword similarity.
        """
        if not movies:
            return []
        
        # Parse the input title for keywords
        title_words = set(self._normalize_title(movie_title).split())
        
        scored_movies = []
        for movie in movies:
            score = 0.0
            movie_title_normalized = self._normalize_title(movie.get('title', ''))
            
            # Skip if it's the same movie (fuzzy)
            if SequenceMatcher(None, self._normalize_title(movie_title), movie_title_normalized).ratio() > 0.9:
                continue
            
            # Check title word overlap
            movie_words = set(movie_title_normalized.split())
            overlap = title_words.intersection(movie_words)
            score += len(overlap) * 0.3
            
            # Check overview for keywords
            overview = movie.get('overview', '').lower()
            for word in title_words:
                if len(word) > 3 and word in overview:
                    score += 0.1
            
            if score > 0:
                scored_movies.append((movie.get('id'), score))
        
        # Sort by score and return top N
        scored_movies.sort(key=lambda x: x[1], reverse=True)
        return scored_movies[:n_recommendations]
    
    def sentiment_based_recommendations(
        self, 
        movies: List[Dict], 
        min_sentiment: float = 0.0,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float, float]]:
        """
        Sentiment-based NLP recommendations.
        Analyzes review sentiment and recommends highly positive movies.
        """
        movie_sentiments = []
        
        for movie in movies:
            # Analyze overview sentiment
            overview = movie.get('overview', '')
            if overview:
                blob = TextBlob(overview)
                sentiment = blob.sentiment.polarity
            else:
                sentiment = 0.0
            
            # Analyze reviews if available
            if 'reviews' in movie and movie['reviews']:
                if isinstance(movie['reviews'], dict) and 'results' in movie['reviews']:
                    review_sentiments = []
                    for review in movie['reviews']['results'][:5]:
                        content = review.get('content', '')
                        if content:
                            review_blob = TextBlob(content[:1000])  # Limit for performance
                            review_sentiments.append(review_blob.sentiment.polarity)
                    
                    if review_sentiments:
                        sentiment = (sentiment + np.mean(review_sentiments)) / 2
            
            vote_average = movie.get('vote_average', 0)
            
            if sentiment >= min_sentiment:
                movie_sentiments.append((
                    movie.get('title', 'Unknown'),
                    sentiment,
                    vote_average
                ))
        
        # Sort by sentiment and rating
        movie_sentiments.sort(key=lambda x: (x[1], x[2]), reverse=True)
        
        return movie_sentiments[:n_recommendations]
    
    def collaborative_filtering_simple(
        self, 
        user_ratings: Dict[str, float],
        all_movies: List[Dict],
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Simple collaborative filtering based on user ratings.
        Recommends movies similar to highly-rated ones.
        """
        if not user_ratings:
            return []
        
        # Get movies user liked (rating >= 4)
        liked_movies = [title for title, rating in user_ratings.items() if rating >= 4]
        
        if not liked_movies:
            return []
        
        # Find similar movies using content-based approach
        recommendations = {}
        
        for movie_title in liked_movies:
            similar = self.content_based_recommendations(movie_title, n_recommendations)
            for movie_id, score in similar:
                # Get title from movie_id
                movie_data = next((m for m in all_movies if m.get('id') == movie_id), None)
                if movie_data:
                    title = movie_data.get('title')
                    if title and title not in user_ratings:  # Don't recommend already rated movies
                        if title in recommendations:
                            recommendations[title] = max(recommendations[title], score)
                        else:
                            recommendations[title] = score
        
        # Sort by similarity score
        sorted_recs = sorted(
            recommendations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        return sorted_recs
    
    def hybrid_recommendations(
        self,
        movie_title: str = None,
        user_ratings: Dict[str, float] = None,
        all_movies: List[Dict] = None,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Hybrid recommendation system combining multiple approaches.
        """
        recommendations = {}
        
        # Content-based recommendations