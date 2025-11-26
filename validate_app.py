"""
Validate that the Streamlit app can be imported and has no syntax errors
"""
import sys
import os

# Suppress Streamlit warnings for testing
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'

print("="*60)
print("Validating Streamlit Application")
print("="*60)

# Test 1: Import app module
print("\n1. Testing app.py import...")
try:
    # We can't actually run streamlit in this test, but we can validate imports
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Check for required imports
    required_imports = [
        'import streamlit',
        'from tmdb_client import TMDBClient',
        'from recommendation_engine import RecommendationEngine',
        'from movie_filters import MovieFilters',
        'from enhanced_features import'
    ]
    
    for imp in required_imports:
        if imp not in content:
            print(f"  ✗ Missing import: {imp}")
            sys.exit(1)
    
    print("  ✓ All required imports present")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 2: Check main structure
print("\n2. Testing app structure...")
try:
    required_functions = [
        'def main():',
        'def show_home():',
        'def show_search_and_filter():',
        'def show_ai_recommendations():',
        'def show_nlp_query():',
        'def show_visualizations():',
        'def show_trending():',
        'def show_watchlist():',
        'def show_comparison():',
    ]
    
    for func in required_functions:
        if func not in content:
            print(f"  ✗ Missing function: {func}")
            sys.exit(1)
    
    print("  ✓ All required functions present")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 3: Check page configuration
print("\n3. Testing Streamlit configuration...")
try:
    if 'st.set_page_config' not in content:
        print("  ✗ Missing page configuration")
        sys.exit(1)
    
    if 'page_title' not in content:
        print("  ✗ Missing page title")
        sys.exit(1)
    
    print("  ✓ Streamlit configuration present")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 4: Check session state usage
print("\n4. Testing session state management...")
try:
    session_state_vars = [
        'tmdb_client',
        'recommendation_engine',
        'watchlist_manager',
        'genres',
        'movies_cache'
    ]
    
    for var in session_state_vars:
        if f"'{var}'" not in content and f'"{var}"' not in content:
            print(f"  ✗ Missing session state variable: {var}")
            sys.exit(1)
    
    print("  ✓ Session state properly configured")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 5: Check error handling
print("\n5. Testing error handling...")
try:
    if 'if st.session_state.tmdb_client is None:' not in content:
        print("  ✗ Missing API key error handling")
        sys.exit(1)
    
    if 'st.error' not in content:
        print("  ✗ Missing error display")
        sys.exit(1)
    
    print("  ✓ Error handling implemented")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 6: Check all pages are accessible
print("\n6. Testing page navigation...")
try:
    pages = [
        '"🏠 Home"',
        '"🔍 Search & Filter"',
        '"🤖 AI Recommendations"',
        '"💬 NLP Query"',
        '"📊 Visualizations"',
        '"🔥 Trending"',
        '"📝 My Watchlist"',
        '"⚖️ Compare Movies"'
    ]
    
    for page in pages:
        if page not in content:
            print(f"  ✗ Missing page: {page}")
            sys.exit(1)
    
    print("  ✓ All navigation pages present")
except Exception as e:
    print(f"  ✗ Error: {e}")
    sys.exit(1)

# Test 7: Validate syntax
print("\n7. Testing Python syntax...")
try:
    import py_compile
    py_compile.compile('app.py', doraise=True)
    print("  ✓ No syntax errors")
except py_compile.PyCompileError as e:
    print(f"  ✗ Syntax error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("✓ All app validation tests passed!")
print("="*60)
print("\nThe Streamlit app is ready to run.")
print("To start the app: streamlit run app.py")
