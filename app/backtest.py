import json
import os
import yfinance as yf
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'events.json')

def load_events():
    with open(DB_PATH, 'r') as f:
        return json.load(f)

def backtest():
    events = load_events()
    results = []

    for event in events:
        if event.get("auto_logged"):
            continue

        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        end_date = event_date + timedelta(days=35)

        try:
            spy = yf.download("SPY", start=event_date, end=end_date, progress=False)

            if len(spy) < 2:
                continue

            actual_t1 = round(((spy["Close"].iloc[1] - spy["Close"].iloc[0]) / spy["Close"].iloc[0]) * 100, 2)
            actual_t5 = round(((spy["Close"].iloc[min(5, len(spy)-1)] - spy["Close"].iloc[0]) / spy["Close"].iloc[0]) * 100, 2)
            actual_t30 = round(((spy["Close"].iloc[-1] - spy["Close"].iloc[0]) / spy["Close"].iloc[0]) * 100, 2)

            predicted_t1 = event["sp500_t1"]
            predicted_t5 = event["sp500_t5"]
            predicted_t30 = event["sp500_t30"]

            actual_t1 = float(actual_t1.iloc[0] if hasattr(actual_t1, 'iloc') else actual_t1)
            actual_t5 = float(actual_t5.iloc[0] if hasattr(actual_t5, 'iloc') else actual_t5)
            actual_t30 = float(actual_t30.iloc[0] if hasattr(actual_t30, 'iloc') else actual_t30)

            results.append({
                "event": event["event"],
                "date": event["date"],
                "category": event["category"],
                "predicted_t1": predicted_t1,
                "actual_t1": actual_t1,
                "error_t1": round(abs(predicted_t1 - actual_t1), 2),
                "predicted_t5": predicted_t5,
                "actual_t5": actual_t5,
                "error_t5": round(abs(predicted_t5 - actual_t5), 2),
                "predicted_t30": predicted_t30,
                "actual_t30": actual_t30,
                "error_t30": round(abs(predicted_t30 - actual_t30), 2),
                "direction_correct_t30": (predicted_t30 < 0) == (actual_t30 < 0)
            })

        except Exception as e:
            print(f"Skipping {event['event']}: {e}")
            continue

    results.sort(key=lambda x: (not x["direction_correct_t30"], x["error_t30"]))
    return results


def print_backtest_summary(results):
    if not results:
        print("No results to summarize.")
        return

    avg_error_t30 = sum(r["error_t30"] for r in results) / len(results)
    direction_accuracy = sum(1 for r in results if r["direction_correct_t30"]) / len(results) * 100

    print(f"\n--- BACKTEST SUMMARY ---")
    print(f"Events tested: {len(results)}")
    print(f"Avg prediction error (T+30): {round(avg_error_t30, 2)}%")
    print(f"Direction accuracy (T+30): {round(direction_accuracy, 1)}%")
    print(f"\n--- PER EVENT ---\n")

    for r in results:
        direction = "✓" if r["direction_correct_t30"] else "✗"
        print(f"{direction} {r['event']} ({r['date']})")
        print(f"  T+30 → Predicted: {r['predicted_t30']}% | Actual: {r['actual_t30']}% | Error: {r['error_t30']}%")


if __name__ == "__main__":
    print("Running backtest — fetching actual market data for all historical events...")
    results = backtest()
    print_backtest_summary(results)