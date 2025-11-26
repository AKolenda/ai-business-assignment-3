# Changelog - Movie Recommendation System Fixes

## Version 2.0 - Bug Fixes and Enhancements

### Issues Fixed

#### 1. Watchlist State Management
**Problem**: Adding movies to watchlist from search/filter + AI recommendations caused page reload and lost search context.

**Solution**: 
- Implemented session state variables (`search_results`, `filtered_results`, `trending_results`) to preserve context
- Removed unnecessary `st.rerun()` calls after adding to watchlist
- Success messages now show inline without page refresh

#### 2. Trending Movies Filtering
**Problem**: No way to filter trending movies by rating.

**Solution**:
- Added ⚙️ (gear icon) expandable filter section to Trending page
- Implemented minimum rating slider filter
- Results persist in session state

#### 3. "Find Similar" Button Navigation
**Problem**: "Find Similar" button only worked from search page and didn't navigate properly.

**Solution**:
- Clicking "Find Similar" now sets movie title in session state
- Automatically navigates to AI Recommendations page
- Auto-triggers content-based recommendation search
- Works from all pages (search, trending, watchlist)

#### 4. Advanced Filters UX
**Problem**: Advanced filters were not intuitive and cluttered the interface.

**Solution**:
- Wrapped filters in expandable "📋 Filter Options" section
- Added emoji icons to filter categories (📅, ⭐, ⏱️, 🎭)
- Clearer button text: "Apply Filters & Search"
- Better visual organization

#### 5. Top Actors Visualization
**Problem**: Graph was not descriptive enough.

**Solution**:
- Added interactive hover tooltips showing movie titles
- Color gradient based on appearance count
- Shows up to 5 movies per actor with "+ X more" indicator
- Dynamic height based on number of actors
- Color bar legend for appearance count
- Subtitle instructing users to hover for details

#### 6. NLP Query Enhancement
**Problem**: Basic pattern matching was limited in understanding natural language queries.

**Solution**:
- Integrated OpenRouter API with model `tngtech/deepseek-r1t2-chimera:free`
- AI-powered query understanding for better parameter extraction
- Fallback to basic pattern matching if API not configured
- In-app API key configuration option
- Better error handling

### Technical Improvements

1. **Session State Management**
   - Added 7 new session state variables for context preservation
   - Page navigation now uses session state
   - Search/filter results cached between interactions

2. **OpenRouter Integration**
   - New `OpenRouterClient` class in `enhanced_features.py`
   - Configurable via environment variable or UI
   - Model: `tngtech/deepseek-r1t2-chimera:free`
   - 30-second timeout for API calls
   - Graceful error handling

3. **UI/UX Enhancements**
   - Better emoji usage for visual cues
   - Expandable sections for cleaner interface
   - Improved success/info messages with emojis
   - Enhanced data visualizations

### API Key Configuration

Two API keys are now supported:

1. **TMDB_API_KEY** (Required)
   - Get from: https://www.themoviedb.org/settings/api
   - Used for: Movie data and metadata

2. **OPENROUTER_API_KEY** (Optional)
   - Get from: https://openrouter.ai/
   - Used for: Enhanced NLP query understanding
   - Falls back to basic pattern matching if not configured

### Files Modified

- `app.py`: Core application logic, state management, UI improvements
- `enhanced_features.py`: OpenRouter client, enhanced visualizations
- `.env.example`: Added OpenRouter API key template

### Breaking Changes

None. All changes are backward compatible.

### Migration Guide

1. Update your `.env` file or Streamlit secrets to include `OPENROUTER_API_KEY` (optional)
2. No code changes needed for existing deployments
3. All features work with or without OpenRouter API key

### Testing Recommendations

1. Test watchlist operations from different pages
2. Verify "Find Similar" works from search, trending, and watchlist
3. Test trending page filter functionality
4. Hover over top actors chart to see movie titles
5. Try NLP queries with and without OpenRouter API key

