from textblob import TextBlob

def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "sentiment": sentiment,
        "score": round(polarity, 3)
    }


def get_severity(headline):
    headline_lower = headline.lower()

    high_keywords = [
        "war", "invasion", "crash", "collapse", "crisis", "catastrophe",
        "emergency", "recession", "panic", "default", "bankruptcy"
    ]
    medium_keywords = [
        "tension", "concern", "risk", "warning", "slowdown", "dispute",
        "sanction", "protest", "uncertainty", "threat"
    ]

    for kw in high_keywords:
        if kw in headline_lower:
            return "high"
    for kw in medium_keywords:
        if kw in headline_lower:
            return "medium"
    return "low"


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ingestion import get_news

    news = get_news()
    print("--- SENTIMENT + SEVERITY ---\n")
    for article in news:
        result = get_sentiment(article["title"])
        severity = get_severity(article["title"])
        print(f"[{result['sentiment'].upper()} | {severity.upper()}] {article['title']}")
        print(f"  polarity score: {result['score']}\n")