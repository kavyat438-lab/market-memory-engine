CATEGORIES = {
    "geopolitical": [
        "war", "invasion", "conflict", "military", "attack", "strike",
        "sanction", "missile", "troops", "iran", "russia", "ukraine", "nato",
        "geopolitical", "tension", "crisis", "diplomat", "treaty", "coup",
        "protest", "riot", "terror", "nuclear", "weapon", "strait", "hormuz",
        "tariff", "trade war", "embargo", "espionage", "sovereignty"
    ],
    "monetary_policy": [
        "rate hike", "interest rate", "federal reserve", "fed", "inflation",
        "rate cut", "basis points", "powell", "central bank", "tightening",
        "monetary", "quantitative", "liquidity", "yield", "bond", "treasury",
        "hawkish", "dovish", "repo rate", "rbi", "ecb", "boe", "deflation",
        "cpi", "pce", "price index", "borrowing cost", "easy rate"
    ],
    "recession_risk": [
        "recession", "gdp", "slowdown", "contraction", "unemployment",
        "layoffs", "downturn", "economic crisis", "stagflation", "default",
        "bankruptcy", "debt ceiling", "fiscal", "deficit", "austerity",
        "consumer sentiment", "retail sales", "job cuts", "hiring freeze",
        "economic outlook", "growth forecast", "limbo", "cracks", "resilient"
    ],
    "energy_crisis": [
        "oil", "crude", "opec", "gas", "energy", "strait of hormuz",
        "pipeline", "fuel", "petroleum", "lng", "natural gas", "refinery",
        "petrochemical", "energy supply", "power crisis", "coal", "renewables",
        "energy transition", "carbon", "electricity", "grid"
    ],
    "market_sentiment": [
        "rally", "crash", "sell off", "bull", "bear", "volatility",
        "short squeeze", "correction", "surge", "plunge", "slips", "drops",
        "gains", "losses", "rebound", "selloff", "panic", "fear", "greed",
        "overvalued", "undervalued", "momentum", "breakout", "support",
        "resistance", "crossroads", "stuck", "limbo", "jitters", "soars"
    ]
}

def classify(headline):
    headline_lower = headline.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = sum(1 for kw in keywords if kw in headline_lower)
        if score > 0:
            scores[category] = score

    if not scores:
        return "unclassified"

    return max(scores, key=scores.get)


if __name__ == "__main__":
    from ingestion import get_news
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    news = get_news()
    print("--- CLASSIFIED HEADLINES ---\n")
    for article in news:
        category = classify(article["title"])
        print(f"[{category.upper()}] {article['title']}")