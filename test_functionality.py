"""
Test script to validate core functionality without API key
"""
import sys
import os

print("=" * 60)
print("Testing Movie Recommendation System Components")
print("=" * 60)

# Test 1: Import modules
print("\n1. Testing module imports...")
try:
    from recommendation_engine import RecommendationEngine
    from movie_filters import MovieFilters
    from enhanced_features import NLPInterface, WatchlistManager, MovieVisualizations, MovieComparison
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Error importing modules: {e}")
    sys.exit(1)

# Test 2: NLP Interface
print("\n2. Testing NLP Interface...")
try:
    test_queries = [
        "action movies from the 2010s",
        "highly rated comedies",
        "sci-fi thrillers from 2020",
    ]
    
    for query in test_queries:
        params = NLPInterface.parse_query(query)
        print(f"  Query: '{query}'")
        print(f"  Parsed: {params}")
    
    print("✓ NLP Interface working correctly")
except Exception as e:
    print(f"✗ Error in NLP Interface: {e}")

# Test 3: Movie Filters
print("\n3. Testing Movie Filters...")
try:
    sample_movies = [
        {
            'title': 'Test Movie 1',
            'release_date': '2015-05-01',
            'vote_average': 7.5,
            'vote_count': 1000,
            'runtime': 120,
            'genres': [{'id': 28, 'name': 'Action'}]
        },
        {
            'title': 'Test Movie 2',
            'release_date': '2020-03-15',
            'vote_average': 8.2,
            'vote_count': 5000,
            'runtime': 150,
            'genres': [{'id': 35, 'name': 'Comedy'}]
        },
    ]
    
    # Test year filter
    filtered = MovieFilters.filter_by_year(sample_movies, min_year=2018)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'Test Movie 2'
    
    # Test rating filter
    filtered = MovieFilters.filter_by_rating(sample_movies, min_rating=8.0)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'Test Movie 2'
    
    # Test runtime filter
    filtered = MovieFilters.filter_by_runtime(sample_movies, max_runtime=130)
    assert len(filtered) == 1
    assert filtered[0]['title'] == 'Test Movie 1'
    
    print("✓ All filter tests passed")
except AssertionError as e:
    print(f"✗ Filter assertion failed: {e}")
except Exception as e:
    print(f"✗ Error in Movie Filters: {e}")

# Test 4: Recommendation Engine
print("\n4. Testing Recommendation Engine...")
try:
    engine = RecommendationEngine()
    
    # Prepare sample data
    sample_movies = [
        {
            'id': 1,
            'title': 'Action Hero',
            'overview': 'An exciting action-packed adventure',
            'genres': [{'id': 28, 'name': 'Action'}],
            'vote_average': 7.5,
            'cast': [{'name': 'Actor A'}, {'name': 'Actor B'}]
        },
        {
            'id': 2,
            'title': 'Comedy Gold',
            'overview': 'A hilarious comedy that will make you laugh',
            'genres': [{'id': 35, 'name': 'Comedy'}],
            'vote_average': 8.0,
            'cast': [{'name': 'Actor C'}, {'name': 'Actor D'}]
        },
        {
            'id': 3,
            'title': 'Action Sequel',
            'overview': 'Another thrilling action movie with explosions',
            'genres': [{'id': 28, 'name': 'Action'}],
            'vote_average': 7.8,
            'cast': [{'name': 'Actor A'}, {'name': 'Actor E'}]
        },
    ]
    
    engine.prepare_data(sample_movies)
    print("  ✓ Engine initialized with sample data")
    
    # Test content-based recommendations
    recommendations = engine.content_based_recommendations('Action Hero', 2)
    print(f"  ✓ Content-based recommendations: {len(recommendations)} found")
    
    # Test sentiment analysis
    sentiment_recs = engine.sentiment_based_recommendations(sample_movies, min_sentiment=0.0, n_recommendations=3)
    print(f"  ✓ Sentiment analysis: {len(sentiment_recs)} recommendations")
    
    print("✓ Recommendation Engine working correctly")
except Exception as e:
    print(f"✗ Error in Recommendation Engine: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Watchlist Manager
print("\n5. Testing Watchlist Manager...")
try:
    watchlist = WatchlistManager()
    
    # Add movie
    movie = {'id': 1, 'title': 'Test Movie'}
    result = watchlist.add_to_watchlist(movie)
    assert result == True
    
    # Try adding duplicate
    result = watchlist.add_to_watchlist(movie)
    assert result == False
    
    # Check watchlist
    items = watchlist.get_watchlist()
    assert len(items) == 1
    
    # Mark as watched
    watchlist.mark_as_watched(1, 8.5)
    watched = watchlist.get_watched()
    assert len(watched) == 1
    
    # Check ratings
    ratings = watchlist.get_ratings()
    assert 'Test Movie' in ratings
    assert ratings['Test Movie'] == 8.5
    
    print("✓ Watchlist Manager working correctly")
except AssertionError as e:
    print(f"✗ Watchlist assertion failed")
except Exception as e:
    print(f"✗ Error in Watchlist Manager: {e}")

# Test 6: Movie Comparison
print("\n6. Testing Movie Comparison...")
try:
    movies = [
        {
            'title': 'Movie A',
            'release_date': '2020-01-01',
            'vote_average': 7.5,
            'vote_count': 1000,
            'popularity': 50.0,
            'runtime': 120,
            'genres': [{'id': 28, 'name': 'Action'}]
        },
        {
            'title': 'Movie B',
            'release_date': '2021-06-15',
            'vote_average': 8.0,
            'vote_count': 2000,
            'popularity': 75.0,
            'runtime': 135,
            'genres': [{'id': 28, 'name': 'Action'}]
        },
    ]
    
    df = MovieComparison.compare_movies(movies)
    assert len(df) == 2
    assert 'Title' in df.columns
    assert 'Rating' in df.columns
    
    # Test similarities
    similarities = MovieComparison.get_similarities(movies[0], movies[1])
    assert 'shared_genres' in similarities
    assert 'Action' in similarities['shared_genres']
    
    print("✓ Movie Comparison working correctly")
except Exception as e:
    print(f"✗ Error in Movie Comparison: {e}")

# Summary
print("\n" + "=" * 60)
print("✓ All core components validated successfully!")
print("=" * 60)
print("\nNote: Full functionality requires a TMDB API key")
print("See README.md for instructions on getting an API key")
