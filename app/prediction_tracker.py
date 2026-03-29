import json
import os
from datetime import datetime

PREDICTIONS_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'predictions.json')

def load_predictions():
    if not os.path.exists(PREDICTIONS_PATH):
        return []
    with open(PREDICTIONS_PATH, 'r') as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)

def save_predictions(predictions):
    with open(PREDICTIONS_PATH, 'w') as f:
        json.dump(predictions, f, indent=2)

def log_prediction(article, category, severity, scenario):
    predictions = load_predictions()

    # avoid duplicate logging
    for p in predictions:
        if p["headline"] == article["title"]:
            return False

    prediction = {
        "headline": article["title"],
        "date_logged": datetime.today().strftime("%Y-%m-%d"),
        "category": category,
        "severity": severity,
        "predicted_sp500_t30": scenario["average"]["sp500"],
        "predicted_gold_t30": scenario["average"]["gold"],
        "predicted_oil_t30": scenario["average"]["oil"],
        "worst_sp500_t30": scenario["worst"]["sp500"],
        "best_sp500_t30": scenario["best"]["sp500"],
        "actual_sp500_t30": None,
        "actual_gold_t30": None,
        "actual_oil_t30": None,
        "verified": False
    }

    predictions.append(prediction)
    save_predictions(predictions)
    return True


def verify_predictions():
    import yfinance as yf
    from datetime import timedelta

    predictions = load_predictions()
    updated = 0

    for p in predictions:
        if p["verified"]:
            continue

        date_logged = datetime.strptime(p["date_logged"], "%Y-%m-%d")
        days_elapsed = (datetime.today() - date_logged).days

        if days_elapsed < 30:
            continue

        # fetch actual market data
        start = date_logged
        end = date_logged + timedelta(days=35)

        try:
            spy = yf.download("SPY", start=start, end=end, progress=False)
            gold = yf.download("GLD", start=start, end=end, progress=False)
            oil = yf.download("USO", start=start, end=end, progress=False)

            if len(spy) >= 2:
                spy_return = round(((spy["Close"].iloc[-1] - spy["Close"].iloc[0]) / spy["Close"].iloc[0]) * 100, 2)
                p["actual_sp500_t30"] = float(spy_return.iloc[0] if hasattr(spy_return, 'iloc') else spy_return)

            if len(gold) >= 2:
                gold_return = round(((gold["Close"].iloc[-1] - gold["Close"].iloc[0]) / gold["Close"].iloc[0]) * 100, 2)
                p["actual_gold_t30"] = float(gold_return.iloc[0] if hasattr(gold_return, 'iloc') else gold_return)

            if len(oil) >= 2:
                oil_return = round(((oil["Close"].iloc[-1] - oil["Close"].iloc[0]) / oil["Close"].iloc[0]) * 100, 2)
                p["actual_oil_t30"] = float(oil_return.iloc[0] if hasattr(oil_return, 'iloc') else oil_return)

            p["verified"] = True
            updated += 1

        except Exception as e:
            print(f"Error verifying: {p['headline']} — {e}")
            continue

    save_predictions(predictions)
    return updated


if __name__ == "__main__":
    print("Verifying predictions...")
    updated = verify_predictions()
    print(f"Updated {updated} predictions with actual data")

    predictions = load_predictions()
    verified = [p for p in predictions if p["verified"]]
    print(f"\nVerified predictions: {len(verified)}")
    for p in verified:
        print(f"\nHeadline: {p['headline']}")
        print(f"Predicted S&P T+30: {p['predicted_sp500_t30']}% | Actual: {p['actual_sp500_t30']}%")