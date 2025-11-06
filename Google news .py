import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob
import plotly.express as px

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="F&O Stock News Tracker", layout="wide")
st.title("📰 F&O Stock News Dashboard")
st.markdown("Stay updated with the latest headlines and trends in top F&O stocks.")

API_KEY = st.secrets.get("N_
