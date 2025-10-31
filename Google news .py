import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# --------------------------
# CONFIG
# --------------------------
API_KEY = st.secrets.get("NEWS_API_KEY")  # Add key in Streamlit secrets
BASE_URL = "https://newsapi.org/v2/everything"

# List of popular F&O stocks (you can expand this)
FO_STOCKS = [
    "Reliance Industries", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
    "SBI", "Bharti Airtel", "Hindustan Unilever", "HDFC", "Adani Enterprises",
    "ITC", "Kotak Mahindra Bank", "Axis Bank", "Tata Motors", "ONGC"
]

# --------------------------
# FUNCTIONS
# --------------------------

def get_date_range(period: str):
    today = datetime.now()
    if period == "Last Week":
        start = today - timedelta(weeks=1)
    elif period == "Last Month":
        start = today - timedelta(days=30)
    elif period == "Last 3 Months":
        start = today - timedelta(days=90)
    elif period == "Last 6 Months":
        start = today - timedelta(days=180)
    else:
        start = today - timedelta(days=7)
    return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


def fetch_news(stock, start_date, end_date):
    params = {
        "q": stock,
        "from": start_date,
        "to": end_date,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": API_KEY,
        "pageSize": 5,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    if data.get("status") != "ok":
        return []
    return data.get("articles", [])


# --------------------------
# STREAMLIT UI
# --------------------------

st.set_page_config(page_title="F&O Stock News Tracker", layout="wide")

st.title("📰 F&O Stock News Dashboard")
st.markdown("Get the latest news for top F&O stocks over selected time ranges.")

time_period = st.selectbox(
    "Select Time Range",
    ["Last Week", "Last Month", "Last 3 Months", "Last 6 Months"]
)

selected_stocks = st.multiselect(
    "Select F&O Stocks",
    FO_STOCKS,
    default=["Reliance Industries", "TCS", "Infosys"]
)

if st.button("Fetch News"):
    start, end = get_date_range(time_period)
    all_news = []

    with st.spinner("Fetching news..."):
        for stock in selected_stocks:
            articles = fetch_news(stock, start, end)
            for a in articles:
                all_news.append({
                    "Stock": stock,
                    "Title": a["title"],
                    "Source": a["source"]["name"],
                    "Published At": a["publishedAt"][:10],
                    "URL": a["url"]
                })

    if all_news:
        df = pd.DataFrame(all_news)
        st.dataframe(df)
    else:
        st.warning("No news found for the selected period and stocks.")

st.markdown("---")
st.caption("Powered by Google News API | Built with ❤️ using Streamlit")
