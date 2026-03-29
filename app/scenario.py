import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

def load_events():
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def get_scenario(category, severity):
    events = load_events()
    matched = [e for e in events if e["category"] == category]

    if not matched:
        return None

    sp500_t30_values = [e["sp500_t30"] for e in matched]
    gold_t30_values = [e["gold_t30"] for e in matched]
    oil_t30_values = [e["oil_t30"] for e in matched]

    worst_sp500 = min(sp500_t30_values)
    best_sp500 = max(sp500_t30_values)
    avg_sp500 = round(sum(sp500_t30_values) / len(sp500_t30_values), 2)

    worst_gold = min(gold_t30_values)
    best_gold = max(gold_t30_values)
    avg_gold = round(sum(gold_t30_values) / len(gold_t30_values), 2)

    worst_oil = min(oil_t30_values)
    best_oil = max(oil_t30_values)
    avg_oil = round(sum(oil_t30_values) / len(oil_t30_values), 2)

    # severity multiplier
    multiplier = {"high": 1.2, "medium": 1.0, "low": 0.8}.get(severity, 1.0)

    return {
        "worst": {
            "sp500": round(worst_sp500 * multiplier, 2),
            "gold": round(best_gold * multiplier, 2),
            "oil": round(worst_oil * multiplier, 2)
        },
        "average": {
            "sp500": avg_sp500,
            "gold": avg_gold,
            "oil": avg_oil
        },
        "best": {
            "sp500": round(best_sp500 * multiplier, 2),
            "gold": round(worst_gold * multiplier, 2),
            "oil": round(best_oil * multiplier, 2)
        }
    }


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ingestion import get_news
    from classifier import classify
    from sentiment import get_severity

    news = get_news()
    seen = set()
    print("--- SCENARIO ENGINE ---\n")
    for article in news:
        category = classify(article["title"])
        severity = get_severity(article["title"])
        if category == "unclassified" or category in seen:
            continue
        seen.add(category)

        result = get_scenario(category, severity)
        if result:
            print(f"Headline: {article['title']}")
            print(f"Category: {category} | Severity: {severity}")
            print(f"WORST  → S&P: {result['worst']['sp500']}% | Gold: {result['worst']['gold']}% | Oil: {result['worst']['oil']}%")
            print(f"AVG    → S&P: {result['average']['sp500']}% | Gold: {result['average']['gold']}% | Oil: {result['average']['oil']}%")
            print(f"BEST   → S&P: {result['best']['sp500']}% | Gold: {result['best']['gold']}% | Oil: {result['best']['oil']}%")
            print()