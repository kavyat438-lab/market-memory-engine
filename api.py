from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from ingestion import get_news, get_both_markets
from classifier import classify
from pattern_engine import get_historical_reaction
from sentiment import get_sentiment, get_severity
from similarity import find_best_match
from scenario import get_scenario
from auto_logger import auto_log_event
from prediction_tracker import log_prediction, load_predictions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))

@app.get("/api/markets")
def markets():
    df = get_both_markets()
    return df.to_dict(orient="records")

@app.get("/api/news")
def news():
    articles = get_news()
    results = []
    for article in articles:
        category = classify(article["title"])
        if category == "unclassified":
            continue
        reaction = get_historical_reaction(category)
        sentiment = get_sentiment(article["title"])
        severity = get_severity(article["title"])
        match = find_best_match(article["title"])
        scenario = get_scenario(category, severity)

        auto_log_event(article, category, severity, reaction)
        if scenario:
            log_prediction(article, category, severity, scenario)

        results.append({
            "title": article["title"],
            "source": article["source"],
            "published_at": article["published_at"][:10],
            "url": article["url"],
            "category": category,
            "sentiment": sentiment,
            "severity": severity,
            "reaction": reaction,
            "match": match if match["match_score"] >= 40 else None,
            "scenario": scenario
        })
    return results

@app.get("/api/predictions")
def predictions():
    return load_predictions()

_backtest_cache = None

@app.get("/api/backtest")
def run_backtest():
    global _backtest_cache
    if _backtest_cache is not None:
        return _backtest_cache
    from backtest import backtest
    _backtest_cache = backtest()
    return _backtest_cache

app.mount("/static", StaticFiles(directory="static"), name="static")