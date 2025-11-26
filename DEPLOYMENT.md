# Deployment Guide

This guide covers deploying the Movie Recommendation System to various cloud platforms.

## Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy Streamlit applications.

### Steps:

1. **Push your code to GitHub** (already done)

2. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Create a new app**
   - Click "New app"
   - Select your repository: `AKolenda/Ai-for-business-assignment-3`
   - Branch: `main` (or your preferred branch)
   - Main file path: `app.py`

4. **Add secrets**
   - Click "Advanced settings"
   - In the "Secrets" section, add:
   ```toml
   TMDB_API_KEY = "your_actual_api_key_here"
   ```

5. **Deploy**
   - Click "Deploy"
   - Your app will be live in a few minutes!

### Custom Domain (Optional)

Once deployed, you can add a custom domain in the app settings.

## Hugging Face Spaces

### Steps:

1. **Create a Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Streamlit" as the SDK
   - Name your space

2. **Upload files**
   - Upload all `.py` files
   - Upload `requirements.txt`
   - Upload `.streamlit/config.toml`

3. **Add secrets**
   - Go to Settings → Repository secrets
   - Add: `TMDB_API_KEY` with your API key value

4. **Create README.md for Space**
   ```yaml
   ---
   title: Movie Recommender
   emoji: 🎬
   colorFrom: red
   colorTo: blue
   sdk: streamlit
   sdk_version: 1.29.0
   app_file: app.py
   pinned: false
   ---
   ```

5. Your app will build and deploy automatically!

## Render

### Steps:

1. **Create account on Render**
   - Go to [render.com](https://render.com)
   - Sign up/Sign in

2. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure service**
   - **Name**: movie-recommender (or your choice)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

4. **Add environment variables**
   - Add: `TMDB_API_KEY` with your API key value

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

## Heroku

### Steps:

1. **Install Heroku CLI**
   ```bash
   # On macOS
   brew tap heroku/brew && brew install heroku
   
   # On Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku app**
   ```bash
   heroku login
   heroku create your-movie-recommender
   ```

3. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port \$PORT --server.address 0.0.0.0" > Procfile
   ```

4. **Create setup.sh**
   ```bash
   cat > setup.sh << 'EOF'
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = \$PORT
   enableCORS = false
   " > ~/.streamlit/config.toml
   EOF
   ```

5. **Update Procfile**
   ```
   web: sh setup.sh && streamlit run app.py
   ```

6. **Set environment variables**
   ```bash
   heroku config:set TMDB_API_KEY=your_api_key_here
   ```

7. **Deploy**
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

## Google Cloud Run

### Steps:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8080
   
   CMD streamlit run app.py --server.port 8080 --server.address 0.0.0.0
   ```

2. **Build and push**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/movie-recommender
   ```

3. **Deploy**
   ```bash
   gcloud run deploy movie-recommender \
     --image gcr.io/PROJECT_ID/movie-recommender \
     --platform managed \
     --set-env-vars TMDB_API_KEY=your_api_key_here
   ```

## Docker (Self-Hosting)

### Steps:

1. **Create Dockerfile** (same as Google Cloud Run above)

2. **Build image**
   ```bash
   docker build -t movie-recommender .
   ```

3. **Run container**
   ```bash
   docker run -p 8501:8080 \
     -e TMDB_API_KEY=your_api_key_here \
     movie-recommender
   ```

## Environment Variables

All platforms require the following environment variable:

- `TMDB_API_KEY`: Your TMDB API key

## Troubleshooting

### Common Issues:

1. **ModuleNotFoundError**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **API Key Not Found**
   - Verify environment variable name: `TMDB_API_KEY`
   - Check secrets are properly configured on the platform

3. **Port Issues**
   - Streamlit Cloud and Hugging Face handle ports automatically
   - For other platforms, ensure port configuration matches

4. **Memory Issues**
   - Reduce cache size in the app
   - Use smaller datasets for initial load
   - Consider upgrading to a paid tier

## Performance Optimization

For better performance in production:

1. **Enable caching**
   - Already implemented with `@st.cache_data` (if needed)
   - Consider Redis for distributed caching

2. **Reduce initial data load**
   - Load fewer pages of movies initially
   - Implement lazy loading

3. **Optimize images**
   - Use smaller poster sizes
   - Implement lazy image loading

4. **Database integration** (Optional)
   - Store frequently accessed data in a database
   - Reduce API calls to TMDB

## Monitoring

- **Streamlit Cloud**: Built-in analytics
- **Heroku**: Use Heroku metrics or add-ons
- **Render**: Built-in metrics dashboard
- **Custom**: Add Google Analytics or similar

## Cost Considerations

- **Streamlit Cloud**: Free tier available
- **Hugging Face Spaces**: Free for public spaces
- **Render**: Free tier with limitations
- **Heroku**: Free tier discontinued, paid plans available
- **TMDB API**: Free tier includes 1000 requests per day

---

Choose the platform that best fits your needs. Streamlit Cloud is recommended for beginners due to its simplicity and integration with Streamlit.
