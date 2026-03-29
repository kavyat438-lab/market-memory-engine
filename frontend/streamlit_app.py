import streamlit as st
import sys
import os
import plotly.graph_objects as go
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from ingestion import get_news, get_market_data, get_both_markets
from classifier import classify
from pattern_engine import get_historical_reaction
from sentiment import get_sentiment, get_severity
from similarity import find_best_match
from scenario import get_scenario
from prediction_tracker import log_prediction, load_predictions
from auto_logger import auto_log_event
from backtest import backtest

st.set_page_config(page_title="Market Memory", layout="wide", page_icon="📊")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.main { background-color: #0d1117; }

.mm-header {
    padding: 1.5rem 0 0.5rem 0;
    border-bottom: 1px solid #1e3a5f;
    margin-bottom: 1.5rem;
}

.mm-title {
    font-size: 1.6rem;
    font-weight: 600;
    color: #e6edf4;
    letter-spacing: -0.3px;
    margin: 0;
}

.mm-caption {
    font-size: 0.8rem;
    color: #6c97be;
    margin: 0.2rem 0 0 0;
}

.mm-metric-card {
    background: #0f1f35;
    border: 1px solid #1e3a5f;
    border-radius: 6px;
    padding: 1rem 1.2rem;
}

.mm-metric-label {
    font-size: 0.72rem;
    color: #6c97be;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
}

.mm-metric-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #e6edf4;
}

.mm-section-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: #6c97be;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1e3a5f;
}

.mm-tag {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 3px;
    letter-spacing: 0.3px;
}

.tag-geo { background: #0f2744; color: #5486b4; border: 1px solid #1e3a5f; }
.tag-monetary { background: #0f2744; color: #9dbad4; border: 1px solid #1e3a5f; }
.tag-recession { background: #2a1a1a; color: #e07070; border: 1px solid #3a2a2a; }
.tag-energy { background: #1a2a1a; color: #70c070; border: 1px solid #2a3a2a; }
.tag-sentiment { background: #2a2a1a; color: #c0b060; border: 1px solid #3a3a2a; }
.tag-unclassified { background: #1a1a1a; color: #888; border: 1px solid #2a2a2a; }

.mm-severity-high { color: #e07070; font-size: 0.72rem; font-weight: 500; }
.mm-severity-medium { color: #c0b060; font-size: 0.72rem; font-weight: 500; }
.mm-severity-low { color: #70c070; font-size: 0.72rem; font-weight: 500; }

.mm-match-bar {
    background: #0b1a2e;
    border-left: 3px solid #0b5394;
    border-radius: 0 4px 4px 0;
    padding: 0.6rem 1rem;
    font-size: 0.78rem;
    color: #9dbad4;
    margin-bottom: 0.8rem;
}

.mm-data-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    color: #6c97be;
    padding: 0.2rem 0;
    border-bottom: 1px solid #1a2a3a;
}

.mm-scenario-worst {
    background: #2a1a1a;
    border: 1px solid #3a2020;
    border-radius: 4px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    color: #e07070;
}

.mm-scenario-avg {
    background: #1a1f0f;
    border: 1px solid #2a3020;
    border-radius: 4px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    color: #a0b870;
}

.mm-scenario-best {
    background: #0f2020;
    border: 1px solid #1a3030;
    border-radius: 4px;
    padding: 0.7rem 1rem;
    font-size: 0.78rem;
    color: #70c0a0;
}

.mm-scenario-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.3rem;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="mm-header"><p class="mm-title">Market Memory</p><p class="mm-caption">Real-time geopolitical event tracker — pattern-matched market impact analysis</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Live Analysis", "Prediction Tracker", "Backtest"])

TAG_CLASS = {
    "geopolitical": "tag-geo",
    "monetary_policy": "tag-monetary",
    "recession_risk": "tag-recession",
    "energy_crisis": "tag-energy",
    "market_sentiment": "tag-sentiment",
    "unclassified": "tag-unclassified"
}

with tab1:

    st.markdown('<p class="mm-section-title">Global Markets — Last 7 Days</p>', unsafe_allow_html=True)
    markets = get_both_markets()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=markets["date"], y=markets["SPY"],
        name="SPY (USD)", yaxis="y1",
        line=dict(color="#3b75a9", width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=markets["date"], y=markets["NIFTY"],
        name="NIFTY 50 (INR)", yaxis="y2",
        line=dict(color="#6c97be", width=1.5, dash="dot")
    ))
    fig.update_layout(
        yaxis=dict(title="SPY (USD)", side="left", gridcolor="#1e3a5f", color="#6c97be", title_font=dict(size=11)),
        yaxis2=dict(title="NIFTY 50 (INR)", side="right", overlaying="y", gridcolor="#1e3a5f", color="#6c97be", title_font=dict(size=11)),
        legend=dict(x=0, y=1.1, orientation="h", font=dict(size=11, color="#9dbad4")),
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0a1628",
        font=dict(color="#9dbad4", family="DM Sans"),
        xaxis=dict(gridcolor="#1e3a5f", color="#6c97be")
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.spinner(""):
        news = get_news()

    categories_found = []
    sentiments_found = []
    severities_found = []

    for article in news:
        cat = classify(article["title"])
        if cat == "unclassified":
            continue
        categories_found.append(cat)
        sentiments_found.append(get_sentiment(article["title"])["sentiment"])
        severities_found.append(get_severity(article["title"]))

    st.markdown('<p class="mm-section-title">Today\'s Market Pulse</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Headlines</div><div class="mm-metric-value">{len(news)}</div></div>', unsafe_allow_html=True)
    with c2:
        top_cat = max(set(categories_found), key=categories_found.count).replace("_", " ").title() if categories_found else "—"
        st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Top Category</div><div class="mm-metric-value" style="font-size:1.1rem">{top_cat}</div></div>', unsafe_allow_html=True)
    with c3:
        dom_sent = max(set(sentiments_found), key=sentiments_found.count).title() if sentiments_found else "—"
        st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Sentiment</div><div class="mm-metric-value" style="font-size:1.1rem">{dom_sent}</div></div>', unsafe_allow_html=True)
    with c4:
        high_sev = severities_found.count("high") if severities_found else 0
        st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">High Severity</div><div class="mm-metric-value" style="color:#e07070">{high_sev}</div></div>', unsafe_allow_html=True)

    st.markdown('<p class="mm-section-title">Live News Analysis</p>', unsafe_allow_html=True)

    for article in news:
        category = classify(article["title"])
        if category == "unclassified":
            continue
        reaction = get_historical_reaction(category)
        sentiment = get_sentiment(article["title"])
        severity = get_severity(article["title"])

        tag_class = TAG_CLASS.get(category, "tag-unclassified")
        sev_class = f"mm-severity-{severity}"
        cat_label = category.replace("_", " ").upper()

        with st.expander(f"{article['title']}"):
            st.markdown(f'<span class="mm-tag {tag_class}">{cat_label}</span>&nbsp;&nbsp;<span class="{sev_class}">{severity.upper()} SEVERITY</span>&nbsp;&nbsp;<span style="font-size:0.72rem;color:#6c97be">{article["source"]} · {article["published_at"][:10]}</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            match = find_best_match(article["title"])
            if match['match_score'] >= 40:
                st.markdown(f'<div class="mm-match-bar">Closest historical parallel: <strong>{match["matched_event"]}</strong> ({match["match_score"]}% match) — S&P moved {match["sp500_t30"]}% over 30 days &nbsp;·&nbsp; Oil {match["oil_t30"]}% &nbsp;·&nbsp; Gold {match["gold_t30"]}%</div>', unsafe_allow_html=True)

            if reaction:
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.markdown(f"""
                    <div style="font-size:0.72rem;color:#6c97be;margin-bottom:0.4rem;font-weight:500;text-transform:uppercase;letter-spacing:0.5px">S&P 500 Avg Reaction · {reaction['matched_events']} events matched</div>
                    <div style="display:flex;gap:1.5rem">
                        <div><div style="font-size:0.68rem;color:#6c97be">T+1</div><div style="font-size:1.1rem;font-weight:600;color:#e6edf4">{reaction['avg_sp500_t1']}%</div></div>
                        <div><div style="font-size:0.68rem;color:#6c97be">T+5</div><div style="font-size:1.1rem;font-weight:600;color:#e6edf4">{reaction['avg_sp500_t5']}%</div></div>
                        <div><div style="font-size:0.68rem;color:#6c97be">T+30</div><div style="font-size:1.1rem;font-weight:600;color:#e6edf4">{reaction['avg_sp500_t30']}%</div></div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_r2:
                    st.markdown(f"""
                    <div style="font-size:0.72rem;color:#6c97be;margin-bottom:0.4rem;font-weight:500;text-transform:uppercase;letter-spacing:0.5px">Gold & Oil T+30</div>
                    <div style="display:flex;gap:1.5rem">
                        <div><div style="font-size:0.68rem;color:#6c97be">Gold</div><div style="font-size:1.1rem;font-weight:600;color:#e6edf4">{reaction['avg_gold_t30']}%</div></div>
                        <div><div style="font-size:0.68rem;color:#6c97be">Oil</div><div style="font-size:1.1rem;font-weight:600;color:#e6edf4">{reaction['avg_oil_t30']}%</div></div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            auto_log_event(article, category, severity, reaction)
            scenario = get_scenario(category, severity)
            if scenario:
                log_prediction(article, category, severity, scenario)
                st.markdown('<div style="font-size:0.72rem;color:#6c97be;font-weight:500;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:0.5rem">Scenario Analysis · T+30</div>', unsafe_allow_html=True)
                s1, s2, s3 = st.columns(3)
                with s1:
                    st.markdown(f'<div class="mm-scenario-worst"><div class="mm-scenario-label">Worst Case</div>S&P {scenario["worst"]["sp500"]}% &nbsp;·&nbsp; Oil {scenario["worst"]["oil"]}% &nbsp;·&nbsp; Gold {scenario["worst"]["gold"]}%</div>', unsafe_allow_html=True)
                with s2:
                    st.markdown(f'<div class="mm-scenario-avg"><div class="mm-scenario-label">Average Case</div>S&P {scenario["average"]["sp500"]}% &nbsp;·&nbsp; Oil {scenario["average"]["oil"]}% &nbsp;·&nbsp; Gold {scenario["average"]["gold"]}%</div>', unsafe_allow_html=True)
                with s3:
                    st.markdown(f'<div class="mm-scenario-best"><div class="mm-scenario-label">Best Case</div>S&P {scenario["best"]["sp500"]}% &nbsp;·&nbsp; Oil {scenario["best"]["oil"]}% &nbsp;·&nbsp; Gold {scenario["best"]["gold"]}%</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("Read article →", article["url"])

with tab2:
    st.markdown('<p class="mm-section-title">Prediction Tracker</p>', unsafe_allow_html=True)
    st.caption("Predictions logged by the system — verified after 30 days against actual market data")

    predictions = load_predictions()

    if not predictions:
        st.info("No predictions logged yet.")
    else:
        verified = [p for p in predictions if p["verified"]]
        pending = [p for p in predictions if not p["verified"]]

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Total Predictions</div><div class="mm-metric-value">{len(predictions)}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Verified</div><div class="mm-metric-value">{len(verified)}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Pending</div><div class="mm-metric-value">{len(pending)}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if verified:
            st.markdown('<p class="mm-section-title">Verified</p>', unsafe_allow_html=True)
            for p in verified:
                with st.expander(p['headline']):
                    st.write(f"**Date:** {p['date_logged']} · **Category:** {p['category']} · **Severity:** {p['severity']}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Predicted S&P T+30", f"{p['predicted_sp500_t30']}%")
                    c2.metric("Actual S&P T+30", f"{p['actual_sp500_t30']}%")
                    diff = round(p['actual_sp500_t30'] - p['predicted_sp500_t30'], 2)
                    c3.metric("Difference", f"{diff}%", delta=f"{diff}%")

        if pending:
            st.markdown('<p class="mm-section-title">Pending · verified after 30 days</p>', unsafe_allow_html=True)
            for p in pending:
                with st.expander(p['headline']):
                    st.write(f"**Date:** {p['date_logged']} · **Category:** {p['category']} · **Severity:** {p['severity']}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Predicted S&P T+30", f"{p['predicted_sp500_t30']}%")
                    c2.metric("Worst Case", f"{p['worst_sp500_t30']}%")
                    c3.metric("Best Case", f"{p['best_sp500_t30']}%")

with tab3:
    st.markdown('<p class="mm-section-title">Backtesting</p>', unsafe_allow_html=True)
    st.caption("Direction accuracy and prediction error across all historical events")

    if st.button("Run Backtest"):
        with st.spinner("Fetching market data..."):
            results = backtest()

        if not results:
            st.error("No results returned.")
        else:
            avg_error = round(sum(r["error_t30"] for r in results) / len(results), 2)
            direction_acc = round(sum(1 for r in results if r["direction_correct_t30"]) / len(results) * 100, 1)

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Events Tested</div><div class="mm-metric-value">{len(results)}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Direction Accuracy</div><div class="mm-metric-value">{direction_acc}%</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="mm-metric-card"><div class="mm-metric-label">Avg Prediction Error</div><div class="mm-metric-value">{avg_error}%</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<p class="mm-section-title">Per Event Results</p>', unsafe_allow_html=True)

            for r in results:
                direction = "✓" if r["direction_correct_t30"] else "✗"
                with st.expander(f"{direction} {r['event']} ({r['date']})"):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Predicted T+30", f"{r['predicted_t30']}%")
                    c2.metric("Actual T+30", f"{r['actual_t30']}%")
                    c3.metric("Error", f"{r['error_t30']}%")
                    c4.metric("Direction", "Correct" if r["direction_correct_t30"] else "Wrong")