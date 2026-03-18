#Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import functions
from src.data_loader import collect_price_data
from src.risk_metrics import calculate_log_returns, calculate_volatility, calculate_var_95, calculate_sharpe
from src.monte_carlo import run_monte_carlo, plot_monte_carlo
from src.stress_test import run_stress_test, plot_stress_test

# Page config
st.set_page_config(
    page_title="Financial Risk Analyzer",
    page_icon="💼",
    layout="wide"
)

# Title
st.title("Financial Risk Analyzer")
st.markdown("Analyze portfolio risk using Monte Carlo simulation and historical stress testing.")

# Sidebar
st.sidebar.header("Portfolio Settings")

# Tickers input
tickers_input = st.sidebar.text_input(
    "Enter Tickers (comma separated)",
    value="VOO, SPY, AAPL"
)
tickers = [t.strip() for t in tickers_input.split(",")]

# Weights input
st.sidebar.subheader("Portfolio Weights")
st.sidebar.caption("Must add up to 1.0")

weights = []
for ticker in tickers:
    weight = st.sidebar.number_input(
        f"{ticker} weight",
        min_value=0.0,
        max_value=1.0,
        value=round(1/len(tickers), 2),
        step=0.05
    )
    weights.append(weight)

# Warning if weights don't add up to 1
total_weight = sum(weights)
if abs(total_weight - 1.0) > 0.01:
    st.sidebar.warning(f"⚠️ Weights sum to {total_weight:.2f} — should equal 1.0")

# Date range
start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp("2020-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp("2026-01-01"))

# Risk free rate
risk_free_rate = st.sidebar.slider(
    "Risk Free Rate (%)",
    min_value=0.0,
    max_value=10.0,
    value=4.5,
    step=0.1
) / 100

# Run button
run = st.sidebar.button("Run Analysis")

if run:
    # Validate weights
    if abs(sum(weights) - 1.0) > 0.01:
        st.error("⚠️ Weights must add up to 1.0 before running analysis!")
    else:
        # Loading spinner while data downloads
        with st.spinner("Fetching market data and running analysis..."):

            # 1. Pull user's date range for main analysis
            data = collect_price_data(tickers, str(start_date), str(end_date))

            # 2. Pull long historical range for stress tests
            historical_data = collect_price_data(tickers, "2007-01-01", "2023-12-31")

            # 3. Calculate log returns
            log_returns = calculate_log_returns(data)
            log_returns = log_returns.dropna()

            # 4. Calculate risk metrics
            volatility = calculate_volatility(log_returns)
            VaR = calculate_var_95(log_returns, weights)
            sharpe = calculate_sharpe(log_returns, volatility.mean(), weights, risk_free_rate)

        # ── Results Section ──
        st.subheader("Portfolio Risk Metrics")

        # Display metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Annualized Volatility (Avg)", f"{volatility.mean():.2%}")
        col2.metric("VaR 95% Confidence", f"{VaR:.2%}")
        col3.metric("Sharpe Ratio", f"{sharpe:.2f}")

        # Individual volatility per ticker
        st.subheader("Volatility Per Ticker")
        st.dataframe(volatility.rename("Annualized Volatility").to_frame().style.format("{:.2%}"))

        # ── Monte Carlo Section ──
        st.subheader("Monte Carlo Simulation — 10,000 Paths")
        mc_results = run_monte_carlo(log_returns, weights, 10000, 252)
        mc_df = pd.DataFrame(mc_results).T
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        ax1.plot(mc_df, alpha=0.1, color='blue')
        ax1.set_title("Monte Carlo 10,000 Simulations")
        ax1.set_xlabel("Days")
        ax1.set_ylabel("Portfolio Value")
        plt.tight_layout()
        st.pyplot(fig1)
        
        # ── Stress Test Section ──
        st.subheader("Historical Stress Tests")
        st.info("Stress tests use 2007–2023 historical data regardless of date range selected above")

        stress_periods = [
            ("2008-09-01", "2009-03-31", "2008 Financial Crisis"),
            ("2020-02-01", "2020-03-31", "COVID Crash"),
            ("2022-01-01", "2022-12-31", "2022 Rate Hike Selloff")
        ]

        colors = ['blue', 'red', 'green', 'orange', 'purple']

        for start_s, end_s, title_s in stress_periods:
            cr = run_stress_test(historical_data, start_s, end_s, title_s)
            fig, ax = plt.subplots(figsize=(12, 4))
            for i, column in enumerate(cr.columns):
                ax.plot(cr[column], color=colors[i % len(colors)], label=column)
            ax.set_title(f"Stress Test: {title_s}")
            ax.set_xlabel("Date")
            ax.set_ylabel("Returns")
            ax.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
