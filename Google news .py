import streamlit as st
import requests
from datetime import datetime

# -------------------------------
# Streamlit App Configuration
# -------------------------------
st.set_page_config(
    page_title="Google News App",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Google News App")
st.write("Fetch and display the latest news using the News API with more features!")

# -------------------------------
# Load API Key from Streamlit Secrets
# -------------------------------
API_KEY = st.secrets.get("NEWS_API_KEY")

if not API_KEY:
    st.error("⚠️ Missing API key! Add your NEWS_API_KEY in Streamlit Secrets.")
    st.stop()

# -------------------------------
# User Inputs
# -------------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "🌍 Select Country",
    options=["us", "gb", "in", "ca", "au"],
    index=0
)

category = st.sidebar.selectbox(
    "🗂️ Select Category",
    options=["general", "business", "entertainment", "health", "science", "sports", "technology"],
    index=0
)

keyword = st.sidebar.text_input("🔍 Search Keyword (optional)")

num_articles = st.sidebar.slider("📰 Number of Articles to Display", min_value=1, max_value=20, value=5)

from_date = st.sidebar.date_input("From Date", datetime.today())
to_date = st.sidebar.date_input("To Date", datetime.today())

source = st.sidebar.text_input("News Source (optional, e.g., cnn, bbc-news)")

# -------------------------------
# Button to Fetch News
# -------------------------------
if st.button("Get Latest News"):
    st.info(f"Fetching news for {category.title()} in {country.upper()}...")

    url = f"https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={API_KEY}&pageSize={num_articles}"

    if keyword:
        url += f"&q={keyword}"
    if source:
        url += f"&sources={source}"
    if from_date:
        url += f"&from={from_date}"
    if to_date:
        url += f"&to={to_date}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            st.warning("No articles found. Try different filters.")
        else:
            for idx, article in enumerate(articles, start=1):
                st.markdown(f"### {idx}. [{article['title']}]({article['url']})")
                
                if article.get("urlToImage"):
                    st.image(article["urlToImage"], use_container_width=True)
                
                with st.expander("Read More"):
                    st.write(article.get("description", "No description available"))
                    st.write(article.get("content", "No additional content"))
                
                st.caption(f"Source: {article.get('source', {}).get('name', 'Unknown')} | Published: {article.get('publishedAt', 'N/A')}")
                st.write("---")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
