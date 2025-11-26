"""
Movie Recommendation System - Main Streamlit Application
Features: TMDB API, Multiple recommendation approaches, Advanced filters, NLP interface
"""
import streamlit as st
import pandas as pd
from typing import List, Dict
import os
import json
import re

# Import custom modules
from tmdb_client import TMDBClient
from recommendation_engine import RecommendationEngine
from movie_filters import MovieFilters
from enhanced_features import (
    NLPInterface, WatchlistManager, MovieVisualizations, MovieComparison, OpenRouterClient
)

# Page configuration
st.set_page_config(
    page_title="AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .movie-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #e1e5eb;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tmdb_client' not in st.session_state:
    api_key = os.getenv("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY", "")
    if api_key:
        st.session_state.tmdb_client = TMDBClient(api_key)
    else:
        st.session_state.tmdb_client = None

if 'recommendation_engine' not in st.session_state:
    st.session_state.recommendation_engine = RecommendationEngine()

if 'watchlist_manager' not in st.session_state:
    st.session_state.watchlist_manager = WatchlistManager()

if 'genres' not in st.session_state:
    st.session_state.genres = {}

if 'movies_cache' not in st.session_state:
    st.session_state.movies_cache = []

# Initialize state for maintaining search/filter contexts
if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if 'filtered_results' not in st.session_state:
    st.session_state.filtered_results = []

if 'find_similar' not in st.session_state:
    st.session_state.find_similar = None

if 'trending_results' not in st.session_state:
    st.session_state.trending_results = []

if 'last_search_query' not in st.session_state:
    st.session_state.last_search_query = ""

# OpenRouter API configuration
if 'openrouter_api_key' not in st.session_state:
    st.session_state.openrouter_api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")


def fetch_and_cache_movies(num_pages: int = 5):
    """Fetch movies and cache them"""
    if st.session_state.tmdb_client is None:
        return []
    
    if st.session_state.movies_cache:
        return st.session_state.movies_cache
    
    movies = []
    with st.spinner("Fetching movies from TMDB..."):
        for page in range(1, num_pages + 1):
            popular = st.session_state.tmdb_client.get_popular_movies(page)
            if 'results' in popular:
                for movie in popular['results']:
                    # Fetch detailed info
                    details = st.session_state.tmdb_client.get_movie_details(movie['id'])
                    if details:
                        movies.append(details)
            
            top_rated = st.session_state.tmdb_client.get_top_rated_movies(page)
            if 'results' in top_rated:
                for movie in top_rated['results']:
                    details = st.session_state.tmdb_client.get_movie_details(movie['id'])
                    if details and details not in movies:
                        movies.append(details)
    
    st.session_state.movies_cache = movies
    return movies


def display_movie_card(movie: Dict, show_actions: bool = True, key_suffix: str = ""):
    """Display a movie card with details"""
    col1, col2 = st.columns([1, 3])
    
    with col1:
        poster_path = movie.get('poster_path')
        if poster_path:
            st.image(
                f"https://image.tmdb.org/t/p/w200{poster_path}",
                use_column_width=True
            )
    
    with col2:
        st.subheader(movie.get('title', 'Unknown'))
        
        # Metadata
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Rating", f"⭐ {movie.get('vote_average', 0):.1f}")
        with col_b:
            release_date = movie.get('release_date', 'N/A')
            year = release_date[:4] if release_date else 'N/A'
            st.metric("Year", year)
        with col_c:
            runtime = movie.get('runtime', 0)
            st.metric("Runtime", f"{runtime} min" if runtime else 'N/A')
        
        # Genres
        genres = movie.get('genres', [])
        if genres:
            genre_names = [g['name'] for g in genres] if isinstance(genres[0], dict) else genres
            st.write("**Genres:**", " • ".join(genre_names))
        
        # Overview
        overview = movie.get('overview', 'No overview available.')
        st.write(overview[:200] + "..." if len(overview) > 200 else overview)
        
        # Actions
        if show_actions:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button(f"Add to Watchlist", key=f"add_{movie['id']}_{key_suffix}"):
                    if st.session_state.watchlist_manager.add_to_watchlist(movie):
                        st.success("✅ Added to watchlist!")
                    else:
                        st.warning("Already in watchlist")
            with col_btn2:
                if st.button(f"Sentiment Analysis", key=f"sentiment_{movie['id']}_{key_suffix}"):
                    st.session_state[f"show_sentiment_{movie['id']}_{key_suffix}"] = True
    
    # Show sentiment if triggered
    if st.session_state.get(f"show_sentiment_{movie['id']}_{key_suffix}", False):
        # ...existing sentiment analysis code...
        pass


def main():
    """Main application"""
    
    # Title
    st.title("🎬 AI-Powered Movie Recommendation System")
    st.markdown("---")
    
    # Check API key
    if st.session_state.tmdb_client is None:
        st.error("⚠️ TMDB API key not configured!")
        st.info("Please set the TMDB_API_KEY environment variable or add it to Streamlit secrets.")
        st.markdown("""
        **How to get an API key:**
        1. Visit [TMDB](https://www.themoviedb.org/)
        2. Create an account
        3. Go to Settings > API
        4. Request an API key
        """)
        
        # Allow manual input
        api_key_input = st.text_input("Or enter your API key here:", type="password")
        if api_key_input and st.button("Set API Key"):
            st.session_state.tmdb_client = TMDBClient(api_key_input)
            st.success("API key set successfully!")
            st.rerun()
        return
    
    # Fetch genres
    if not st.session_state.genres:
        genres_response = st.session_state.tmdb_client.get_genres()
        if 'genres' in genres_response:
            st.session_state.genres = {g['name']: g['id'] for g in genres_response['genres']}
    
    # Initialize page state
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.radio(
            "Choose a feature:",
            [
                "🏠 Home",
                "🔍 Search & Filter",
                "🤖 AI Recommendations",
                "💬 NLP Query",
                "📊 Visualizations",
                "🔥 Trending",
                "📝 My Watchlist",
                "⚖️ Compare Movies"
            ],
            index=[
                "🏠 Home",
                "🔍 Search & Filter",
                "🤖 AI Recommendations",
                "💬 NLP Query",
                "📊 Visualizations",
                "🔥 Trending",
                "📝 My Watchlist",
                "⚖️ Compare Movies"
            ].index(st.session_state.page) if st.session_state.page in [
                "🏠 Home",
                "🔍 Search & Filter",
                "🤖 AI Recommendations",
                "💬 NLP Query",
                "📊 Visualizations",
                "🔥 Trending",
                "📝 My Watchlist",
                "⚖️ Compare Movies"
            ] else 0
        )
        
        # Update session state page
        st.session_state.page = page
        
        st.markdown("---")
        st.caption("Powered by TMDB API")
    
    # Main content based on selected page
    if page == "🏠 Home":
        show_home()
    elif page == "🔍 Search & Filter":
        show_search_and_filter()
    elif page == "🤖 AI Recommendations":
        show_ai_recommendations()
    elif page == "💬 NLP Query":
        show_nlp_query()
    elif page == "📊 Visualizations":
        show_visualizations()
    elif page == "🔥 Trending":
        show_trending()
    elif page == "📝 My Watchlist":
        show_watchlist()
    elif page == "⚖️ Compare Movies":
        show_comparison()


def show_home():
    """Home page"""
    st.header("Welcome to AI Movie Recommender! 🎬")
    
    st.markdown("""
    ### Features:
    
    #### 🎯 Multiple Recommendation Approaches:
    - **Content-Based Filtering**: Find movies similar to ones you love
    - **Sentiment Analysis**: Discover movies with positive reviews
    - **Collaborative Filtering**: Get recommendations based on your ratings
    - **Hybrid System**: Combines all approaches for best results
    
    #### 🔍 Advanced Filters:
    - **Temporal**: Filter by year, decade
    - **Quality**: Minimum rating, vote count
    - **Content**: Runtime, language
    - **Personnel**: Actors, directors
    - **Genres**: All major genres
    
    #### ✨ Enhanced Features:
    - **NLP Interface**: Ask questions in natural language
    - **Similarity Discovery**: Find movies like your favorites
    - **Personal Watchlist**: Track movies you want to watch
    - **Visualizations**: Beautiful charts and graphs
    - **Trending Movies**: See what's hot right now
    - **Movie Comparisons**: Compare multiple movies side-by-side
    """)
    
    # Quick stats
    st.markdown("---")
    st.subheader("📈 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Features", "6+")
    with col2:
        st.metric("Recommendation Types", "4")
    with col3:
        st.metric("Filter Options", "10+")
    with col4:
        watchlist_count = len(st.session_state.watchlist_manager.get_watchlist())
        st.metric("Your Watchlist", watchlist_count)


def show_search_and_filter():
    """Search and filter page"""
    st.header("🔍 Search & Filter Movies")
    
    # Search bar
    search_query = st.text_input("Search for a movie:", placeholder="Enter movie title...", value=st.session_state.last_search_query)
    
    # Search button
    if st.button("Search", key="search_btn") or (search_query and search_query != st.session_state.last_search_query):
        if search_query:
            st.session_state.last_search_query = search_query
            with st.spinner("Searching..."):
                results = st.session_state.tmdb_client.search_movies(search_query)
                if 'results' in results and results['results']:
                    st.session_state.search_results = []
                    for movie in results['results'][:10]:
                        details = st.session_state.tmdb_client.get_movie_details(movie['id'])
                        if details:
                            st.session_state.search_results.append(details)
                else:
                    st.session_state.search_results = []
    
    # Display search results if available
    if st.session_state.search_results:
        st.success(f"Found {len(st.session_state.search_results)} results")
        
        for movie in st.session_state.search_results:
            display_movie_card(movie)
            st.markdown("---")
    elif st.session_state.last_search_query:
        st.warning("No movies found. Try a different search term.")
    
    st.markdown("---")
    st.subheader("🎛️ Advanced Filters")
    
    # Filters in expandable section for better UX
    with st.expander("📋 Filter Options", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📅 Temporal Filters**")
            min_year = st.number_input("Minimum Year", 1900, 2025, 2000)
            max_year = st.number_input("Maximum Year", 1900, 2025, 2025)
            
            st.write("**⭐ Quality Filters**")
            min_rating = st.slider("Minimum Rating", 0.0, 10.0, 6.0, 0.5)
            min_votes = st.number_input("Minimum Vote Count", 0, 10000, 100)
        
        with col2:
            st.write("**⏱️ Content Specifications**")
            min_runtime = st.number_input("Minimum Runtime (minutes)", 0, 300, 0)
            max_runtime = st.number_input("Maximum Runtime (minutes)", 0, 300, 200)
            
            st.write("**🎭 Genre Filters**")
            selected_genres = st.multiselect(
                "Select Genres",
                list(st.session_state.genres.keys())
            )
    
    if st.button("Apply Filters & Search", type="primary"):
        with st.spinner("Filtering movies..."):
            # Fetch movies
            movies = fetch_and_cache_movies(3)
            
            # Apply filters
            filters = {
                'min_year': min_year,
                'max_year': max_year,
                'min_rating': min_rating,
                'min_votes': min_votes,
                'min_runtime': min_runtime if min_runtime > 0 else None,
                'max_runtime': max_runtime if max_runtime < 300 else None,
            }
            
            if selected_genres:
                filters['genre_names'] = selected_genres
            
            st.session_state.filtered_results = MovieFilters.apply_filters(movies, filters)
    
    # Display filtered results if available
    if st.session_state.filtered_results:
        st.success(f"Found {len(st.session_state.filtered_results)} movies matching your criteria")
        
        for movie in st.session_state.filtered_results[:20]:
            display_movie_card(movie)
            st.markdown("---")


def show_ai_recommendations():
    """AI recommendations page"""
    st.header("🤖 AI-Powered Recommendations")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Content-Based",
        "Sentiment Analysis",
        "Collaborative",
        "Hybrid"
    ])
    
    with tab1:
        st.subheader("Content-Based Filtering")
        st.write("Find movies similar to ones you love based on genres, cast, plot, and more.")
        
        # Check if we came from "Find Similar" button
        default_title = st.session_state.find_similar if st.session_state.find_similar else ""
        movie_title = st.text_input("Enter a movie you like:", value=default_title, key="content_based")
        
        # Auto-trigger search if we came from "Find Similar"
        auto_search = bool(st.session_state.find_similar)
        if st.session_state.find_similar:
            st.session_state.find_similar = None  # Clear the flag
        
        if (movie_title and st.button("Get Recommendations", key="btn_content")) or (movie_title and auto_search):
            with st.spinner("Analyzing movie features..."):
                # Fetch and prepare data
                movies = fetch_and_cache_movies(5)
                st.session_state.recommendation_engine.prepare_data(movies)
                
                # Get recommendations
                recommendations = st.session_state.recommendation_engine.content_based_recommendations(
                    movie_title, 10
                )
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} similar movies!")
                    
                    for idx, (movie_id, score) in enumerate(recommendations):
                        movie_data = next((m for m in movies if m.get('id') == movie_id), None)
                        if movie_data:
                            st.write(f"**Similarity Score:** {score:.2f}")
                            display_movie_card(movie_data, key_suffix=f"ai_rec_{idx}")
                            st.markdown("---")
                else:
                    st.warning("Movie not found in our database. Try another title.")
    
    with tab2:
        st.subheader("Sentiment-Based Recommendations")
        st.write("Discover movies with positive sentiment in reviews and descriptions.")
        
        min_sentiment = st.slider("Minimum Sentiment Score", -1.0, 1.0, 0.2, 0.1)
        
        if st.button("Find Positive Movies", key="btn_sentiment"):
            with st.spinner("Analyzing sentiment..."):
                movies = fetch_and_cache_movies(5)
                
                recommendations = st.session_state.recommendation_engine.sentiment_based_recommendations(
                    movies, min_sentiment, 15
                )
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} movies with positive sentiment!")
                    
                    for title, sentiment, rating in recommendations:
                        movie_data = next((m for m in movies if m.get('title') == title), None)
                        if movie_data:
                            st.write(f"**Sentiment:** {sentiment:.2f} | **Rating:** {rating:.1f}")
                            display_movie_card(movie_data)
                            st.markdown("---")
    
    with tab3:
        st.subheader("Collaborative Filtering")
        st.write("Get recommendations based on your ratings.")
        
        st.info("Rate some movies to get personalized recommendations!")
        
        # Get user ratings
        user_ratings = st.session_state.watchlist_manager.get_ratings()
        
        if user_ratings:
            st.write("**Your Ratings:**")
            for title, rating in user_ratings.items():
                st.write(f"- {title}: {rating:.1f} ⭐")
        
        if st.button("Get Collaborative Recommendations", key="btn_collab"):
            if not user_ratings:
                st.warning("Please rate some movies first! Go to your watchlist to rate movies.")
            else:
                with st.spinner("Finding similar tastes..."):
                    movies = fetch_and_cache_movies(5)
                    st.session_state.recommendation_engine.prepare_data(movies)
                    
                    recommendations = st.session_state.recommendation_engine.collaborative_filtering_simple(
                        user_ratings, movies, 10
                    )
                    
                    if recommendations:
                        st.success(f"Found {len(recommendations)} recommendations based on your ratings!")
                        
                        for title, score in recommendations:
                            movie_data = next((m for m in movies if m.get('title') == title), None)
                            if movie_data:
                                st.write(f"**Match Score:** {score:.2f}")
                                display_movie_card(movie_data)
                                st.markdown("---")
    
    with tab4:
        st.subheader("Hybrid Recommendations")
        st.write("Best of all approaches combined!")
        
        movie_for_hybrid = st.text_input("Base movie (optional):", key="hybrid_movie")
        
        if st.button("Get Hybrid Recommendations", key="btn_hybrid"):
            with st.spinner("Combining all recommendation approaches..."):
                movies = fetch_and_cache_movies(5)
                st.session_state.recommendation_engine.prepare_data(movies)
                
                user_ratings = st.session_state.watchlist_manager.get_ratings()
                
                recommendations = st.session_state.recommendation_engine.hybrid_recommendations(
                    movie_title=movie_for_hybrid if movie_for_hybrid else None,
                    user_ratings=user_ratings if user_ratings else None,
                    all_movies=movies,
                    n_recommendations=10
                )
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} hybrid recommendations!")
                    
                    for title, score in recommendations:
                        movie_data = next((m for m in movies if m.get('title') == title), None)
                        if movie_data:
                            st.write(f"**Hybrid Score:** {score:.2f}")
                            display_movie_card(movie_data)
                            st.markdown("---")
                else:
                    st.info("Add more ratings or specify a base movie for better results.")


def show_nlp_query():
    """NLP query interface with OpenRouter AI"""
    st.header("💬 Natural Language Movie Search")
    st.write("Ask for movies in plain English - powered by AI!")
    
    # Check if OpenRouter API key is configured
    if not st.session_state.openrouter_api_key:
        st.warning("⚠️ OpenRouter API key not configured. Using basic pattern matching.")
        with st.expander("ℹ️ How to configure OpenRouter"):
            st.write("""
            To enable AI-powered natural language understanding:
            1. Set the OPENROUTER_API_KEY environment variable
            2. Or add it to Streamlit secrets
            3. Restart the application
            """)
            api_key_input = st.text_input("Or enter your OpenRouter API key here:", type="password", key="openrouter_key_input")
            if api_key_input and st.button("Set OpenRouter Key"):
                st.session_state.openrouter_api_key = api_key_input
                st.success("API key set successfully!")
                st.rerun()
    
    st.markdown("""
    **Try queries like:**
    - "Show me action movies from the 2010s"
    - "Find highly rated comedies"
    - "Romantic movies from the 90s"
    - "Sci-fi thrillers with good ratings"
    - "What are some good horror movies with at least a 7 rating?"
    """)
    
    query = st.text_area("What kind of movies are you looking for?", height=100)
    
    # Store NLP results in session state
    if "nlp_results" not in st.session_state:
        st.session_state.nlp_results = None
    
    if query and st.button("Search", type="primary"):
        with st.spinner("Understanding your query with AI..."):
            # Use OpenRouter if available for enhanced understanding
            if st.session_state.openrouter_api_key:
                try:
                    openrouter = OpenRouterClient(st.session_state.openrouter_api_key)
                    
                    system_prompt = """You are a movie search assistant. Extract search parameters from user queries.
                    Return ONLY a JSON object with these fields (all optional):
                    - genres: list of genre names (action, comedy, drama, horror, thriller, romance, sci-fi, fantasy, animation, documentary)
                    - year: specific year (integer)
                    - decade: decade value like 1980, 1990, 2000, 2010, 2020 (integer)
                    - min_rating: minimum rating 0-10 (float)
                    - keywords: key search terms (string)
                    
                    Example: {"genres": ["action", "sci-fi"], "decade": 2010, "min_rating": 7.0}
                    """
                    
                    ai_response = openrouter.query(query, system_prompt)
                    
                    # Try to extract JSON from response
                    try:
                        # Look for JSON in the response
                        json_match = re.search(r'\{[^}]+\}', ai_response)
                        if json_match:
                            params = json.loads(json_match.group())
                            st.write("**AI Understood:**", params)
                        else:
                            # Fallback to basic parsing
                            params = NLPInterface.parse_query(query)
                            st.write("**Detected Parameters:**", params)
                    except json.JSONDecodeError:
                        params = NLPInterface.parse_query(query)
                        st.write("**Detected Parameters (fallback):**", params)
                except Exception as e:
                    st.warning(f"AI query failed: {str(e)}. Using basic pattern matching.")
                    params = NLPInterface.parse_query(query)
                    st.write("**Detected Parameters:**", params)
            else:
                # Basic pattern matching fallback
                params = NLPInterface.parse_query(query)
                st.write("**Detected Parameters:**", params)
            
            # Fetch movies
            movies = fetch_and_cache_movies(5)
            
            # Build filters from params
            filters = {}
            
            if 'year' in params:
                filters['min_year'] = params['year']
                filters['max_year'] = params['year']
            
            if 'decade' in params:
                filters['decade'] = params['decade']
            
            if 'min_rating' in params:
                filters['min_rating'] = params['min_rating']
            
            if 'genres' in params:
                filters['genre_names'] = params['genres']
            
            # Apply filters
            if filters:
                filtered_movies = MovieFilters.apply_filters(movies, filters)
            else:
                filtered_movies = movies[:20]
            
            # Generate response
            if filtered_movies:
                response = NLPInterface.generate_response(filtered_movies, query)
                st.success(response)
                
                # Display results
                for idx, movie in enumerate(filtered_movies[:15]):
                    display_movie_card(movie, key_suffix=f"nlp_{idx}")
                    st.markdown("---")
            else:
                st.warning("No movies found matching your criteria. Try adjusting your search!")


def show_visualizations():
    """Visualizations page"""
    st.header("📊 Movie Data Visualizations")
    
    with st.spinner("Loading movie data..."):
        movies = fetch_and_cache_movies(5)
    
    if not movies:
        st.warning("No movie data available.")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Rating Distribution",
        "Genre Analysis",
        "Timeline",
        "Top Actors"
    ])
    
    with tab1:
        st.subheader("Rating Distribution")
        fig = MovieVisualizations.create_rating_distribution(movies)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Genre Distribution")
        fig = MovieVisualizations.create_genre_distribution(movies)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Movies Timeline")
        fig = MovieVisualizations.create_timeline(movies)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Most Frequent Actors")
        fig = MovieVisualizations.create_top_actors_chart(movies)
        st.plotly_chart(fig, use_container_width=True)


def show_trending():
    """Trending movies page"""
    st.header("🔥 Trending Movies")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        time_window = st.radio("Time Period:", ["Today", "This Week"])
    
    with col2:
        # Add filter gear icon functionality
        with st.expander("⚙️ Filters", expanded=False):
            min_rating_trending = st.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.5, key="trending_rating")
    
    window = "day" if time_window == "Today" else "week"
    
    if st.button("Get Trending Movies", type="primary") or not st.session_state.trending_results:
        with st.spinner("Fetching trending movies..."):
            trending = st.session_state.tmdb_client.get_trending_movies(window)
            
            if 'results' in trending and trending['results']:
                st.session_state.trending_results = []
                for movie in trending['results']:
                    details = st.session_state.tmdb_client.get_movie_details(movie['id'])
                    if details:
                        st.session_state.trending_results.append(details)
    
    # Apply rating filter if set
    if st.session_state.trending_results:
        filtered_trending = [m for m in st.session_state.trending_results if m.get('vote_average', 0) >= min_rating_trending]
        
        if filtered_trending:
            st.success(f"🔥 {len(filtered_trending)} trending movies!" + (f" (filtered by rating ≥ {min_rating_trending})" if min_rating_trending > 0 else ""))
            
            for movie in filtered_trending:
                display_movie_card(movie)
                st.markdown("---")
        else:
            st.warning(f"No trending movies found with rating ≥ {min_rating_trending}. Try lowering the filter.")


def show_watchlist():
    """Watchlist management page"""
    st.header("📝 My Watchlist")
    
    tab1, tab2 = st.tabs(["To Watch", "Watched"])
    
    with tab1:
        watchlist = st.session_state.watchlist_manager.get_watchlist()
        
        if not watchlist:
            st.info("Your watchlist is empty. Add movies from search results!")
        else:
            st.success(f"You have {len(watchlist)} movies in your watchlist")
            
            for movie in watchlist:
                display_movie_card(movie, show_actions=False)
                
                col1, col2 = st.columns(2)
                with col1:
                    rating = st.slider(
                        f"Rate this movie",
                        0.0, 10.0, 5.0, 0.5,
                        key=f"rate_{movie['id']}"
                    )
                with col2:
                    if st.button("Mark as Watched", key=f"watched_{movie['id']}"):
                        st.session_state.watchlist_manager.mark_as_watched(
                            movie['id'],
                            rating
                        )
                        st.success("Marked as watched!")
                        st.rerun()
                
                if st.button("Remove", key=f"remove_{movie['id']}"):
                    st.session_state.watchlist_manager.remove_from_watchlist(movie['id'])
                    st.success("Removed from watchlist!")
                    st.rerun()
                
                st.markdown("---")
    
    with tab2:
        watched = st.session_state.watchlist_manager.get_watched()
        
        if not watched:
            st.info("You haven't marked any movies as watched yet.")
        else:
            st.success(f"You've watched {len(watched)} movies")
            
            for movie in watched:
                display_movie_card(movie, show_actions=False)
                
                # Show user's rating
                ratings = st.session_state.watchlist_manager.get_ratings()
                user_rating = ratings.get(movie.get('title'), 0)
                st.write(f"**Your Rating:** {user_rating:.1f} ⭐")
                
                st.markdown("---")


def show_comparison():
    """Movie comparison page"""
    st.header("⚖️ Compare Movies")
    
    st.write("Search and select movies to compare:")
    
    # Search for movies to compare
    search1 = st.text_input("Search for first movie:", key="compare1")
    search2 = st.text_input("Search for second movie:", key="compare2")
    
    selected_movies = []
    
    if search1:
        results = st.session_state.tmdb_client.search_movies(search1)
        if 'results' in results and results['results']:
            movie1 = st.selectbox(
                "Select first movie:",
                results['results'],
                format_func=lambda x: f"{x['title']} ({x.get('release_date', 'N/A')[:4]})",
                key="select1"
            )
            if movie1:
                details1 = st.session_state.tmdb_client.get_movie_details(movie1['id'])
                selected_movies.append(details1)
    
    if search2:
        results = st.session_state.tmdb_client.search_movies(search2)
        if 'results' in results and results['results']:
            movie2 = st.selectbox(
                "Select second movie:",
                results['results'],
                format_func=lambda x: f"{x['title']} ({x.get('release_date', 'N/A')[:4]})",
                key="select2"
            )
            if movie2:
                details2 = st.session_state.tmdb_client.get_movie_details(movie2['id'])
                selected_movies.append(details2)
    
    if len(selected_movies) >= 2:
        st.markdown("---")
        st.subheader("Comparison Results")
        
        # Comparison table
        comparison_df = MovieComparison.compare_movies(selected_movies)
        st.dataframe(comparison_df, use_container_width=True)
        
        # Comparison chart
        fig = MovieVisualizations.create_comparison_chart(selected_movies)
        st.plotly_chart(fig, use_container_width=True)
        
        # Similarities
        if len(selected_movies) == 2:
            st.subheader("Similarities")
            similarities = MovieComparison.get_similarities(selected_movies[0], selected_movies[1])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Shared Genres", len(similarities['shared_genres']))
                if similarities['shared_genres']:
                    st.write(", ".join(similarities['shared_genres']))
            
            with col2:
                st.metric("Rating Difference", f"{similarities['rating_difference']:.1f}")
            
            with col3:
                st.metric("Years Apart", similarities['year_difference'])


if __name__ == "__main__":
    main()
