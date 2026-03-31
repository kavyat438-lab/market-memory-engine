# Market Memory Engine

A full-stack geopolitical market intelligence system that maps real-time macroeconomic and geopolitical headlines to historical market reactions — surfacing probabilistic insights into how S&P 500, NIFTY 50, gold, and oil may respond before price discovery completes.

Built in under a week as a second-year undergraduate project.

---

## What It Does

Markets don't just react to news — they react to patterns. The same type of event (a war, a rate hike, an oil shock) produces surprisingly consistent reactions across decades.

Market Memory reads live headlines, classifies them by event type, finds the closest historical analogues using sentence transformer embeddings, and outputs scenario-based market impact forecasts with backtested accuracy metrics.

---

## Features

- **Live news ingestion** — NewsAPI with geopolitical and macro query filtering
- **NLP classification pipeline** — keyword-based event tagging + TextBlob sentiment scoring + severity heuristics
- **AI similarity matching** — sentence transformer embeddings (all-MiniLM-L6-v2) for cosine similarity between current headlines and historical event corpus
- **Historical pattern engine** — 70+ curated events across geopolitical, monetary policy, recession risk, energy crisis, and market sentiment categories
- **Multi-asset analysis** — S&P 500, NIFTY 50 (India), Gold, Oil reactions at T+1, T+5, and T+30 horizons
- **Scenario engine** — severity-weighted worst / average / best case projections
- **Prediction tracker** — auto-logs forecasts and verifies them against actual market data after 30 days
- **Backtesting** — 60.9% directional accuracy across 64 historical events, 5.17% average prediction error
- **Portfolio Simulator** — enter holdings (Indian NSE or US stocks), fetch live prices via yfinance, track real-time P&L, and receive per-stock event exposure analysis mapped against today's dominant macro themes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI |
| NLP | TextBlob, sentence-transformers (all-MiniLM-L6-v2) |
| Market Data | yfinance |
| News Data | NewsAPI |
| Frontend | HTML, CSS, JavaScript, Chart.js |
| Data | JSON event corpus (hand-curated + auto-logged) |

---

## Project Structure

```
market-memory-engine/
├── api.py                  # FastAPI server — all endpoints
├── app/
│   ├── ingestion.py        # News + market data fetching
│   ├── classifier.py       # Event classification
│   ├── sentiment.py        # Sentiment + severity scoring
│   ├── similarity.py       # Sentence transformer matching
│   ├── pattern_engine.py   # Historical reaction averaging
│   ├── scenario.py         # Scenario generation
│   ├── auto_logger.py      # Auto event logging with quarantine
│   ├── prediction_tracker.py # Prediction logging + verification
│   └── backtest.py         # Backtesting against actual data
├── data/
│   └── events.json         # Historical event database
├── static/
│   └── index.html          # Frontend dashboard
└── frontend/
    └── streamlit_app.py    # Legacy Streamlit UI
```

---

## Setup

```bash
git clone https://github.com/kavyat438-lab/market-memory-engine
cd market-memory-engine
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Create a `.env` file in the root:
```
NEWS_API_KEY=your_newsapi_key_here
```

Get a free API key at [newsapi.org](https://newsapi.org)

Run the server:
```bash
uvicorn api:app --reload
```

Open `http://localhost:8000/static/index.html`

---

## Backtesting Results

Tested across 64 historical events from 2000–2024:

- **Direction accuracy:** 60.9% — system correctly predicted whether markets would move up or down
- **Average prediction error:** 5.17 percentage points
- **Key finding:** The system consistently underestimates post-shock recoveries — markets rebound faster than historical averages suggest, particularly after high-severity events like COVID and 9/11

---

## Disclaimer

This is not a financial prediction tool. It provides probabilistic context based on historical patterns. Past market reactions do not guarantee future outcomes.

---

## Author

**Kavya Thakur** — B.Sc. Electronics (Hons), Hansraj College, University of Delhi

[LinkedIn](https://www.linkedin.com/in/kavya-thakur-2b8bb22b4/) · [GitHub](https://github.com/kavyat438-lab)
