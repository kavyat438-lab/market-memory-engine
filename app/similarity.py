from sentence_transformers import SentenceTransformer, util
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_events():
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def find_best_match(headline):
    events = load_events()
    
    headline_embedding = model.encode(headline, convert_to_tensor=True)
    
    best_score = -1
    best_event = None
    
    for event in events:
        if event.get("auto_logged"):
            from datetime import datetime
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            days_old = (datetime.today() - event_date).days
            if days_old < 30:
                continue
        event_text = f"{event['event']} - {event['description']}"
        event_embedding = model.encode(event_text, convert_to_tensor=True)
        score = util.cos_sim(headline_embedding, event_embedding).item()
        
        if score > best_score:
            best_score = score
            best_event = event
    
    return {
        "matched_event": best_event["event"],
        "match_score": round(best_score * 100, 1),
        "category": best_event["category"],
        "sp500_t30": best_event["sp500_t30"],
        "gold_t30": best_event["gold_t30"],
        "oil_t30": best_event["oil_t30"],
        "date": best_event["date"]
    }


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from ingestion import get_news
    
    news = get_news()
    print("--- AI SIMILARITY MATCHING ---\n")
    for article in news[:5]:
        match = find_best_match(article["title"])
    print(f"Headline: {article['title']}")
    print(f"AI Match: {match['matched_event']} ({match['match_score']}% match) — when this happened, S&P moved {match['sp500_t30']}% over 30 days | Oil: {match['oil_t30']}% | Gold: {match['gold_t30']}%")
    print()