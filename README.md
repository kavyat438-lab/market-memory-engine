# Market Memory Engine

A system that maps real-time geopolitical news to historical market reactions to provide probabilistic insights into how markets may respond.

---

## Features

* Real-time news ingestion (NewsAPI)
* Event classification (geopolitical, monetary, sentiment, severity)
* AI-based historical event matching
* Multi-asset analysis (S&P 500, NIFTY 50, Gold, Oil)
* Scenario modeling (best / base / worst case)
* Prediction tracking and validation system
* Portfolio simulation (in progress)

---

##Core Idea

Markets don’t just react to news — they react to memory.

This system analyzes how similar events affected markets in the past and uses that to provide contextual insights for current events.

---

# How It Works

1. Fetches live news headlines
2. Classifies event type and sentiment
3. Matches event with historical analogues
4. Computes market reactions
5. Generates probabilistic scenarios
6. Tracks predictions vs actual outcomes

---

## Example Insight

> High-severity geopolitical events tend to cause short-term drawdowns, with recovery typically within 30 days.

---

# Tech Stack

* Python
* Streamlit
* Pandas
* yfinance
* NewsAPI

---

##Disclaimer

This is not a financial prediction tool. It provides probabilistic context based on historical patterns.
