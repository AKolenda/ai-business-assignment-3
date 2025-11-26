# Quick Start Guide

Get the Movie Recommendation System running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

## Step 1: Get the Code

```bash
git clone https://github.com/AKolenda/Ai-for-business-assignment-3.git
cd Ai-for-business-assignment-3
```

Or download and extract the ZIP file.

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including Streamlit, scikit-learn, NLTK, etc.

## Step 3: Get a TMDB API Key (Free)

1. Go to https://www.themoviedb.org/signup
2. Create a free account
3. Navigate to Settings → API
4. Request an API key (select "Developer")
5. Fill out the simple form
6. Copy your API key

## Step 4: Configure API Key

Choose one method:

### Method A: Environment Variable (Recommended for local)
```bash
export TMDB_API_KEY="your_api_key_here"
```

### Method B: .env File
```bash
cp .env.example .env
# Edit .env and replace your_api_key_here with your actual key
```

### Method C: Streamlit Secrets (For deployment)
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your key
```

## Step 5: Run the Application

```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## Step 6: Explore Features

Navigate through the sidebar to explore:

1. **🏠 Home** - Overview of features
2. **🔍 Search & Filter** - Search movies with advanced filters
3. **🤖 AI Recommendations** - Try all 4 recommendation approaches
4. **💬 NLP Query** - Ask in natural language
5. **📊 Visualizations** - View data charts
6. **🔥 Trending** - See what's hot
7. **📝 My Watchlist** - Manage your watchlist
8. **⚖️ Compare Movies** - Compare movies side-by-side

## Quick Demo (Without API Key)

If you don't have an API key yet, you can still see the system in action:

```bash
python demo.py
```

This runs a demo with sample data showcasing all major features.

## Troubleshooting

### Issue: "TMDB API key not configured"
**Solution**: Make sure you've set the API key using one of the methods in Step 4.

### Issue: "ModuleNotFoundError"
**Solution**: Run `pip install -r requirements.txt` to install all dependencies.

### Issue: "Port already in use"
**Solution**: Use a different port: `streamlit run app.py --server.port 8502`

### Issue: NLTK data not found
**Solution**: The app downloads it automatically on first run. If issues persist:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Testing the Installation

Run the test suite to verify everything is working:

```bash
python test_functionality.py
```

You should see all tests passing with ✓ marks.

## Next Steps

### Deploy to Streamlit Cloud (Free!)

1. Push your code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repository
4. Add your API key in Secrets
5. Deploy!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Customize the Application

- Edit `app.py` to modify the UI
- Add new recommendation algorithms in `recommendation_engine.py`
- Create custom filters in `movie_filters.py`
- Add new visualizations in `enhanced_features.py`

## Usage Examples

### Example 1: Content-Based Recommendations
1. Go to "🤖 AI Recommendations" → "Content-Based"
2. Enter a movie title like "The Dark Knight"
3. Click "Get Recommendations"
4. See similar movies based on genres, cast, and plot

### Example 2: Natural Language Search
1. Go to "💬 NLP Query"
2. Type: "Show me highly rated action movies from the 2010s"
3. Click "Search"
4. See filtered results matching your query

### Example 3: Build Your Watchlist
1. Search for movies in "🔍 Search & Filter"
2. Click "Add to Watchlist" on movies you want to watch
3. Go to "📝 My Watchlist"
4. Rate movies and mark them as watched
5. Get personalized recommendations based on your ratings

### Example 4: Explore Trending
1. Go to "🔥 Trending"
2. Select "Today" or "This Week"
3. Click "Get Trending Movies"
4. Discover what's popular right now

## Tips for Best Experience

1. **Rate Movies**: Add ratings to get better collaborative filtering recommendations
2. **Try NLP Queries**: The natural language interface is powerful - try complex queries
3. **Use Filters**: Combine multiple filters for precise results
4. **Explore Visualizations**: Check the charts to understand movie trends
5. **Compare Movies**: Use the comparison tool before deciding what to watch

## Need Help?

- Read the full [README.md](README.md) for comprehensive documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guides
- Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details
- Run `python demo.py` to see examples

## System Requirements

- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for dependencies
- **Python**: 3.8, 3.9, 3.10, 3.11, or 3.12
- **Internet**: Required for TMDB API access

## API Rate Limits

TMDB free tier includes:
- 1,000 requests per day
- 40 requests per 10 seconds

The application handles rate limiting gracefully.

---

**You're all set! Enjoy discovering movies! 🎬🍿**
