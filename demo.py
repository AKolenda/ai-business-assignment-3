"""
Demo script to showcase functionality without API key
Generates synthetic movie data for demonstration
"""
import pandas as pd
from recommendation_engine import RecommendationEngine
from movie_filters import MovieFilters
from enhanced_features import NLPInterface, MovieVisualizations, MovieComparison

# Generate sample movie data
def generate_sample_movies():
    """Generate sample movies for demonstration"""
    return [
        {
            'id': 1,
            'title': 'The Dark Knight',
            'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
            'genres': [{'id': 28, 'name': 'Action'}, {'id': 80, 'name': 'Crime'}, {'id': 18, 'name': 'Drama'}],
            'release_date': '2008-07-16',
            'vote_average': 9.0,
            'vote_count': 25000,
            'popularity': 100.0,
            'runtime': 152,
            'cast': [
                {'name': 'Christian Bale'},
                {'name': 'Heath Ledger'},
                {'name': 'Aaron Eckhart'}
            ],
            'director': 'Christopher Nolan',
            'poster_path': '/qJ2tW6WMUDux911r6m7haRef0WH.jpg'
        },
        {
            'id': 2,
            'title': 'Inception',
            'overview': 'Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life.',
            'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}, {'id': 53, 'name': 'Thriller'}],
            'release_date': '2010-07-15',
            'vote_average': 8.8,
            'vote_count': 30000,
            'popularity': 95.0,
            'runtime': 148,
            'cast': [
                {'name': 'Leonardo DiCaprio'},
                {'name': 'Joseph Gordon-Levitt'},
                {'name': 'Ellen Page'}
            ],
            'director': 'Christopher Nolan',
            'poster_path': '/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg'
        },
        {
            'id': 3,
            'title': 'The Shawshank Redemption',
            'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'genres': [{'id': 18, 'name': 'Drama'}, {'id': 80, 'name': 'Crime'}],
            'release_date': '1994-09-23',
            'vote_average': 9.3,
            'vote_count': 22000,
            'popularity': 85.0,
            'runtime': 142,
            'cast': [
                {'name': 'Tim Robbins'},
                {'name': 'Morgan Freeman'},
                {'name': 'Bob Gunton'}
            ],
            'director': 'Frank Darabont',
            'poster_path': '/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg'
        },
        {
            'id': 4,
            'title': 'Interstellar',
            'overview': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity survival.',
            'genres': [{'id': 12, 'name': 'Adventure'}, {'id': 18, 'name': 'Drama'}, {'id': 878, 'name': 'Science Fiction'}],
            'release_date': '2014-11-05',
            'vote_average': 8.6,
            'vote_count': 28000,
            'popularity': 90.0,
            'runtime': 169,
            'cast': [
                {'name': 'Matthew McConaughey'},
                {'name': 'Anne Hathaway'},
                {'name': 'Jessica Chastain'}
            ],
            'director': 'Christopher Nolan',
            'poster_path': '/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg'
        },
        {
            'id': 5,
            'title': 'The Godfather',
            'overview': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
            'genres': [{'id': 80, 'name': 'Crime'}, {'id': 18, 'name': 'Drama'}],
            'release_date': '1972-03-14',
            'vote_average': 9.2,
            'vote_count': 18000,
            'popularity': 80.0,
            'runtime': 175,
            'cast': [
                {'name': 'Marlon Brando'},
                {'name': 'Al Pacino'},
                {'name': 'James Caan'}
            ],
            'director': 'Francis Ford Coppola',
            'poster_path': '/3bhkrj58Vtu7enYsRolD1fZdja1.jpg'
        },
        {
            'id': 6,
            'title': 'Pulp Fiction',
            'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
            'genres': [{'id': 53, 'name': 'Thriller'}, {'id': 80, 'name': 'Crime'}],
            'release_date': '1994-09-10',
            'vote_average': 8.9,
            'vote_count': 25000,
            'popularity': 88.0,
            'runtime': 154,
            'cast': [
                {'name': 'John Travolta'},
                {'name': 'Uma Thurman'},
                {'name': 'Samuel L. Jackson'}
            ],
            'director': 'Quentin Tarantino',
            'poster_path': '/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg'
        },
        {
            'id': 7,
            'title': 'Forrest Gump',
            'overview': 'The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man.',
            'genres': [{'id': 35, 'name': 'Comedy'}, {'id': 18, 'name': 'Drama'}, {'id': 10749, 'name': 'Romance'}],
            'release_date': '1994-06-23',
            'vote_average': 8.8,
            'vote_count': 24000,
            'popularity': 92.0,
            'runtime': 142,
            'cast': [
                {'name': 'Tom Hanks'},
                {'name': 'Robin Wright'},
                {'name': 'Gary Sinise'}
            ],
            'director': 'Robert Zemeckis',
            'poster_path': '/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg'
        },
        {
            'id': 8,
            'title': 'The Matrix',
            'overview': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
            'genres': [{'id': 28, 'name': 'Action'}, {'id': 878, 'name': 'Science Fiction'}],
            'release_date': '1999-03-30',
            'vote_average': 8.7,
            'vote_count': 23000,
            'popularity': 87.0,
            'runtime': 136,
            'cast': [
                {'name': 'Keanu Reeves'},
                {'name': 'Laurence Fishburne'},
                {'name': 'Carrie-Anne Moss'}
            ],
            'director': 'Lana Wachowski',
            'poster_path': '/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg'
        },
    ]


def demo_nlp_interface():
    """Demonstrate NLP interface"""
    print("\n" + "="*60)
    print("DEMO: Natural Language Processing Interface")
    print("="*60)
    
    queries = [
        "action movies from the 2010s",
        "highly rated crime dramas",
        "science fiction thrillers",
        "comedies from the 90s"
    ]
    
    for query in queries:
        params = NLPInterface.parse_query(query)
        print(f"\nQuery: '{query}'")
        print(f"Detected parameters: {params}")


def demo_filters():
    """Demonstrate movie filters"""
    print("\n" + "="*60)
    print("DEMO: Movie Filtering")
    print("="*60)
    
    movies = generate_sample_movies()
    print(f"\nTotal movies: {len(movies)}")
    
    # Filter by year
    filtered = MovieFilters.filter_by_year(movies, min_year=2010)
    print(f"\nMovies from 2010 onwards: {len(filtered)}")
    for m in filtered:
        print(f"  - {m['title']} ({m['release_date'][:4]})")
    
    # Filter by rating
    filtered = MovieFilters.filter_by_rating(movies, min_rating=9.0)
    print(f"\nMovies with rating >= 9.0: {len(filtered)}")
    for m in filtered:
        print(f"  - {m['title']} (⭐ {m['vote_average']})")
    
    # Filter by genre
    filtered = MovieFilters.filter_by_genres(movies, genre_names=['Action'])
    print(f"\nAction movies: {len(filtered)}")
    for m in filtered:
        print(f"  - {m['title']}")


def demo_recommendations():
    """Demonstrate recommendation engine"""
    print("\n" + "="*60)
    print("DEMO: Recommendation Engine")
    print("="*60)
    
    movies = generate_sample_movies()
    engine = RecommendationEngine()
    engine.prepare_data(movies)
    
    # Content-based recommendations
    print("\nContent-Based Recommendations for 'The Dark Knight':")
    recommendations = engine.content_based_recommendations('The Dark Knight', 3)
    for title, score in recommendations:
        print(f"  - {title} (similarity: {score:.3f})")
    
    # Sentiment analysis
    print("\nSentiment-Based Recommendations:")
    sentiment_recs = engine.sentiment_based_recommendations(movies, min_sentiment=0.0, n_recommendations=5)
    for title, sentiment, rating in sentiment_recs:
        print(f"  - {title} (sentiment: {sentiment:.3f}, rating: {rating})")
    
    # Collaborative filtering with sample ratings
    print("\nCollaborative Filtering (based on sample user ratings):")
    user_ratings = {
        'The Dark Knight': 9.0,
        'Inception': 8.5,
        'Interstellar': 8.8
    }
    collab_recs = engine.collaborative_filtering_simple(user_ratings, movies, 3)
    for title, score in collab_recs:
        print(f"  - {title} (match score: {score:.3f})")
    
    # Hybrid recommendations
    print("\nHybrid Recommendations:")
    hybrid_recs = engine.hybrid_recommendations(
        movie_title='The Dark Knight',
        user_ratings=user_ratings,
        all_movies=movies,
        n_recommendations=3
    )
    for title, score in hybrid_recs:
        print(f"  - {title} (hybrid score: {score:.3f})")


def demo_comparison():
    """Demonstrate movie comparison"""
    print("\n" + "="*60)
    print("DEMO: Movie Comparison")
    print("="*60)
    
    movies = generate_sample_movies()
    
    # Compare two movies
    movie1 = movies[0]  # The Dark Knight
    movie2 = movies[1]  # Inception
    
    print(f"\nComparing: '{movie1['title']}' vs '{movie2['title']}'")
    
    similarities = MovieComparison.get_similarities(movie1, movie2)
    print(f"\nShared Genres: {similarities['shared_genres']}")
    print(f"Rating Difference: {similarities['rating_difference']:.1f}")
    print(f"Years Apart: {similarities['year_difference']}")
    
    # Comparison table
    print("\nComparison Table:")
    df = MovieComparison.compare_movies([movie1, movie2])
    print(df.to_string(index=False))


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("MOVIE RECOMMENDATION SYSTEM - DEMO")
    print("="*60)
    print("\nThis demo showcases the system's capabilities using sample data.")
    print("Full functionality requires a TMDB API key.")
    
    demo_nlp_interface()
    demo_filters()
    demo_recommendations()
    demo_comparison()
    
    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print("\nTo use the full application:")
    print("1. Get a TMDB API key from https://www.themoviedb.org/")
    print("2. Set the API key in your environment or .env file")
    print("3. Run: streamlit run app.py")
    print("\nSee README.md for detailed instructions.")


if __name__ == "__main__":
    main()
