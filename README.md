# 🎬 AI-Powered Movie Recommendation System

A comprehensive movie recommendation system powered by AI and machine learning, integrating with The Movie Database (TMDB) API. This application offers multiple recommendation approaches, advanced filtering, natural language processing, and rich visualizations.

## 🌟 Features

### Multiple Recommendation Approaches

1. **Content-Based Filtering**: Recommends movies based on similarity of genres, cast, plot, and keywords
2. **Sentiment-Based NLP**: Analyzes movie overviews and reviews using natural language processing to recommend positively-reviewed movies
3. **Collaborative Filtering**: Provides recommendations based on user ratings and preferences
4. **Hybrid System**: Combines all approaches for optimal recommendations

### Core Filtering Capabilities

- **Temporal Filters**: Filter by year, decade, or date range
- **Quality Filters**: Minimum rating, vote count thresholds
- **Content Specifications**: Runtime duration, original language
- **Personnel Filters**: Search by actors, directors, and crew
- **Genre Filters**: All major movie genres (Action, Comedy, Drama, etc.)

### Enhanced Features

1. **NLP Interface**: Ask for movies in natural language (e.g., "Show me action movies from the 2010s")
2. **Similarity Discovery**: Find movies similar to your favorites
3. **Personal Watchlist**: Manage movies you want to watch and track watched movies
4. **Data Visualizations**:
   - Rating distribution histograms
   - Genre distribution pie charts
   - Movie timeline scatter plots
   - Top actors bar charts
5. **Trending Movies**: View daily and weekly trending movies
6. **Movie Comparisons**: Compare multiple movies side-by-side with detailed metrics

## 🚀 Technology Stack

### Backend

- **Python 3.8+**
- **Streamlit**: Web framework for interactive UI
- **TMDB API**: Movie metadata and information

### NLP & Machine Learning

- **NLTK**: Natural language processing
- **spaCy**: Advanced NLP capabilities
- **TextBlob**: Sentiment analysis
- **scikit-learn**: Machine learning algorithms (TF-IDF, cosine similarity)

### Data Processing & Visualization

- **pandas**: Data manipulation
- **numpy**: Numerical computations
- **plotly**: Interactive visualizations
- **matplotlib & seaborn**: Statistical visualizations

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- TMDB API key (free from [themoviedb.org](https://www.themoviedb.org/))

### Step 1: Clone the Repository

```bash
git clone https://github.com/AKolenda/Ai-for-business-assignment-3.git
cd Ai-for-business-assignment-3
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data

The application will automatically download required NLTK data on first run, but you can pre-download:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 4: Configure API Key

#### Option 1: Environment Variable

```bash
export TMDB_API_KEY="your_api_key_here"
```

#### Option 3: Streamlit Secrets

Create `.streamlit/secrets.toml`:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your API key
```

## 🎯 Usage

### Running Locally

```bash
streamlit run app.py
OR
python3 -m streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Navigation

The application has 8 main sections accessible from the sidebar:

1. **🏠 Home**: Overview and quick stats
2. **🔍 Search & Filter**: Search movies and apply advanced filters
3. **🤖 AI Recommendations**: Access all four recommendation approaches
4. **💬 NLP Query**: Natural language movie search
5. **📊 Visualizations**: View data visualizations
6. **🔥 Trending**: See trending movies
7. **📝 My Watchlist**: Manage your personal watchlist
8. **⚖️ Compare Movies**: Compare movies side-by-side

## 🌐 Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add your TMDB API key in the Secrets section:
   ```toml
   TMDB_API_KEY = "your_api_key_here"
   ```
5. Deploy!

### Hugging Face Spaces

1. Create a new Space on [huggingface.co/spaces](https://huggingface.co/spaces)
2. Select Streamlit as the SDK
3. Upload your code
4. Add API key to Space secrets
5. Your app will be live!

### Render

1. Create a new Web Service on [render.com](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable `TMDB_API_KEY`
6. Deploy!

## 📚 Project Structure

```
Ai-for-business-assignment-3/
├── app.py                      # Main Streamlit application
├── tmdb_client.py              # TMDB API client
├── recommendation_engine.py    # Recommendation algorithms
├── movie_filters.py            # Filtering utilities
├── enhanced_features.py        # NLP, visualizations, watchlist
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets.toml.example   # Secrets template
└── README.md                  # This file
```

## 🔑 Getting a TMDB API Key

1. Visit [themoviedb.org](https://www.themoviedb.org/)
2. Create a free account
3. Go to Settings → API
4. Request an API key (choose "Developer" option)
5. Fill out the required information
6. Copy your API key and add it to the application

## 🎨 Features in Detail

### Content-Based Filtering

Uses TF-IDF vectorization and cosine similarity to find movies with similar:

- Genres
- Plot descriptions
- Keywords
- Cast and crew

### Sentiment Analysis

Analyzes text using TextBlob to determine sentiment polarity:

- Positive sentiment (>0): Uplifting, positive themes
- Negative sentiment (<0): Dark, serious themes
- Neutral sentiment (≈0): Balanced tone

### NLP Query Interface

Understands natural language queries:

- Temporal: "movies from the 90s", "2020 films"
- Genre: "action movies", "romantic comedies"
- Quality: "highly rated", "best movies"
- Combined: "highly rated sci-fi from 2010s"

### Visualizations

Interactive charts using Plotly:

- Histogram of rating distributions
- Pie chart of genre popularity
- Timeline scatter plot of movies
- Bar chart of frequent actors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- All the open-source libraries that made this project possible

## 📞 Support

If you encounter any issues or have questions:

1. Check that your TMDB API key is correctly configured
2. Ensure all dependencies are installed
3. Review the error messages in the console
4. Open an issue on GitHub

---

**Built with ❤️ using Python, Streamlit, and AI/ML technologies**
