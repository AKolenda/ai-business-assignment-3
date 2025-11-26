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
        """Combine movie features into a single string"""
        features = []
        
        # Add genres
        if 'genres' in row and row['genres']:
            if isinstance(row['genres'], list):
                features.extend([g['name'] for g in row['genres']])
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
        if 'cast' in row and row['cast']:
            if isinstance(row['cast'], list):
                features.extend([actor['name'] for actor in row['cast'][:5]])
        
        # Add director
        if 'director' in row and row['director']:
            features.append(str(row['director']))
        
        return ' '.join(features).lower()
    
    def content_based_recommendations(
        self, 
        movie_title: str, 
        n_recommendations: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Content-based filtering recommendations
        Based on movie features similarity
        """
        if self.movies_df is None or self.tfidf_matrix is None:
            return []
        
        # Find movie index
        try:
            idx = self.movies_df[
                self.movies_df['title'].str.lower() == movie_title.lower()
            ].index[0]
        except IndexError:
            return []
        
        # Calculate cosine similarity
        cosine_similarities = cosine_similarity(
            self.tfidf_matrix[idx:idx+1], 
            self.tfidf_matrix
        ).flatten()
        
        # Get top similar movies (excluding the input movie)
        similar_indices = cosine_similarities.argsort()[::-1][1:n_recommendations+1]
        
        recommendations = [
            (self.movies_df.iloc[i]['title'], cosine_similarities[i])
            for i in similar_indices
        ]
        
        return recommendations
    
    def sentiment_based_recommendations(
        self, 
        movies: List[Dict], 
        min_sentiment: float = 0.0,
        n_recommendations: int = 10
    ) -> List[Tuple[str, float, float]]:
        """
        Sentiment-based NLP recommendations
        Analyzes review sentiment and recommends highly positive movies
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
                            review_blob = TextBlob(content)
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
        Simple collaborative filtering based on user ratings
        Recommends movies similar to highly-rated ones
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
            for title, score in similar:
                if title not in user_ratings:  # Don't recommend already rated movies
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
        Hybrid recommendation system combining multiple approaches
        """
        recommendations = {}
        
        # Content-based recommendations
        if movie_title:
            content_recs = self.content_based_recommendations(movie_title, n_recommendations * 2)
            for title, score in content_recs:
                recommendations[title] = recommendations.get(title, 0) + score * 0.4
        
        # Collaborative filtering
        if user_ratings:
            collab_recs = self.collaborative_filtering_simple(
                user_ratings, 
                all_movies or [], 
                n_recommendations * 2
            )
            for title, score in collab_recs:
                recommendations[title] = recommendations.get(title, 0) + score * 0.3
        
        # Sentiment-based boost
        if all_movies:
            sentiment_recs = self.sentiment_based_recommendations(
                all_movies, 
                min_sentiment=0.2,
                n_recommendations=n_recommendations * 2
            )
            for title, sentiment, rating in sentiment_recs:
                if title in recommendations:
                    # Boost score based on sentiment
                    recommendations[title] += sentiment * 0.3
        
        # Sort by combined score
        sorted_recs = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return sorted_recs
    
    def find_similar_movies(
        self,
        movie_title: str,
        n_similar: int = 10,
        similarity_threshold: float = 0.1
    ) -> List[Tuple[str, float]]:
        """Find movies similar to the given movie"""
        similar = self.content_based_recommendations(movie_title, n_similar)
        return [(title, score) for title, score in similar if score >= similarity_threshold]
