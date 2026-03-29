import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

def load_events():
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def get_historical_reaction(category):
    events = load_events()
    from datetime import datetime
    def is_usable(e):
        if e.get("auto_logged"):
            event_date = datetime.strptime(e["date"], "%Y-%m-%d")
            days_old = (datetime.today() - event_date).days
            return days_old >= 30
        return True
    matched = [e for e in events if e["category"] == category and is_usable(e)]

    if not matched:
        return None

    avg_sp500_t1 = sum(e["sp500_t1"] for e in matched) / len(matched)
    avg_sp500_t5 = sum(e["sp500_t5"] for e in matched) / len(matched)
    avg_sp500_t30 = sum(e["sp500_t30"] for e in matched) / len(matched)

    avg_gold_t5 = sum(e["gold_t5"] for e in matched) / len(matched)
    avg_gold_t30 = sum(e["gold_t30"] for e in matched) / len(matched)

    avg_oil_t5 = sum(e["oil_t5"] for e in matched) / len(matched)
    avg_oil_t30 = sum(e["oil_t30"] for e in matched) / len(matched)

    return {
        "category": category,
        "matched_events": len(matched),
        "avg_sp500_t1": round(avg_sp500_t1, 2),
        "avg_sp500_t5": round(avg_sp500_t5, 2),
        "avg_sp500_t30": round(avg_sp500_t30, 2),
        "avg_gold_t5": round(avg_gold_t5, 2),
        "avg_gold_t30": round(avg_gold_t30, 2),
        "avg_oil_t5": round(avg_oil_t5, 2),
        "avg_oil_t30": round(avg_oil_t30, 2),
        "events": [e["event"] for e in matched]
    }


if __name__ == "__main__":
    from classifier import classify
    from ingestion import get_news
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    news = get_news()
    print("--- PATTERN ANALYSIS ---\n")

    seen = set()
    for article in news:
        category = classify(article["title"])
        if category == "unclassified" or category in seen:
            continue
        seen.add(category)

        result = get_historical_reaction(category)
        if result:
            print(f"Headline: {article['title']}")
            print(f"Category: {category.upper()}")
            print(f"Matched {result['matched_events']} historical events: {result['events']}")
            print(f"S&P  → T+1: {result['avg_sp500_t1']}% | T+5: {result['avg_sp500_t5']}% | T+30: {result['avg_sp500_t30']}%")
            print(f"Gold → T+5: {result['avg_gold_t5']}% | T+30: {result['avg_gold_t30']}%")
            print(f"Oil  → T+5: {result['avg_oil_t5']}% | T+30: {result['avg_oil_t30']}%")
            print()