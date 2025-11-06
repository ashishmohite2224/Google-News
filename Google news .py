import streamlit as st
import requests

# -------------------------------
# Streamlit App Configuration
# -------------------------------
st.set_page_config(
    page_title="Google News App",
    page_icon="📰",
    layout="wide"
)

st.title("📰 Google News App")
st.write("Fetch and display the latest top headlines using the News API.")

# -------------------------------
# Load API Key
# -------------------------------
API_KEY = st.secrets.get("NEWS_API_KEY")

if not API_KEY:
    st.error("⚠️ Missing API key! Please add your NEWS_API_KEY in Streamlit Secrets.")
    st.stop()

# -------------------------------
# User Inputs
# -------------------------------
country = st.selectbox(
    "🌍 Select Country",
    options=["us", "gb", "in", "ca", "au"],
    index=0
)

category = st.selectbox(
    "🗂️ Select Category",
    options=[
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ],
    index=0
)

# -------------------------------
# Button to Fetch News
# -------------------------------
if st.button("Get Latest News"):
    st.info(f"Fetching {category.title()} news for {country.upper()}...")

    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country={country}&category={category}&apiKey={API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            st.warning("No articles found. Try another category or country.")
        else:
            for article in articles:
                st.markdown(f"### [{article['title']}]({article['url']})")

                if article.get("urlToImage"):
                    st.image(article["urlToImage"], use_container_width=True)

                if article.get("description"):
                    st.write(article["description"])

                st.caption(f"Source: {article.get('source', {}).get('name', 'Unknown')}")
                st.write("---")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
