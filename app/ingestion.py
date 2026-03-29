import requests
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(query="geopolitical war recession inflation oil federal reserve markets", num_articles=25):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": num_articles,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"],
            "url": article["url"]
        })
    return articles


def get_market_data(ticker="SPY", days=7):
    end = datetime.today()
    start = end - timedelta(days=days)
    df = yf.download(ticker, start=start, end=end)
    df = df[["Close"]].reset_index()
    df.columns = ["date", "close"]
    return df

def get_both_markets(days=7):
    spy = get_market_data("SPY", days)
    nifty = get_market_data("^NSEI", days)
    spy = spy.rename(columns={"close": "SPY"})
    nifty = nifty.rename(columns={"close": "NIFTY"})
    merged = spy.merge(nifty, on="date", how="inner")
    return merged


if __name__ == "__main__":
    print("--- NEWS ---")
    news = get_news()
    for n in news:
        print(n["title"], "|", n["published_at"])

    print("\n--- MARKET DATA ---")
    market = get_market_data()
    print(market)