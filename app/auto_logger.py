import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

def load_events():
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def save_events(events):
    with open(DB_PATH, 'w') as f:
        json.dump(events, f, indent=2)

def event_already_exists(title, events):
    title_lower = title.lower()
    for e in events:
        if e["event"].lower() in title_lower or title_lower in e["event"].lower():
            return True
    return False

def auto_log_event(article, category, severity, reaction):
    if severity != "high":
        return False
    if category == "unclassified":
        return False
    if reaction is None:
        return False

    events = load_events()

    if event_already_exists(article["title"], events):
        return False

    new_event = {
        "event": article["title"][:80],
        "date": article["published_at"][:10],
        "category": category,
        "description": article["title"],
        "sp500_t1": reaction["avg_sp500_t1"],
        "sp500_t5": reaction["avg_sp500_t5"],
        "sp500_t30": reaction["avg_sp500_t30"],
        "gold_t1": reaction["avg_gold_t5"],
        "gold_t5": reaction["avg_gold_t5"],
        "gold_t30": reaction["avg_gold_t30"],
        "oil_t1": reaction["avg_oil_t5"],
        "oil_t5": reaction["avg_oil_t5"],
        "oil_t30": reaction["avg_oil_t30"],
        "severity": severity,
        "auto_logged": True
    }

    events.append(new_event)
    save_events(events)
    return True


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ingestion import get_news
    from classifier import classify
    from sentiment import get_severity
    from pattern_engine import get_historical_reaction

    news = get_news()
    print("--- AUTO LOGGER ---\n")
    logged_count = 0
    for article in news:
        category = classify(article["title"])
        severity = get_severity(article["title"])
        reaction = get_historical_reaction(category)
        logged = auto_log_event(article, category, severity, reaction)
        if logged:
            print(f"Logged: {article['title'][:80]}")
            logged_count += 1

    print(f"\nTotal new events logged: {logged_count}")