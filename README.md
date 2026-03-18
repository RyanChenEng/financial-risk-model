# Financial Risk Modeling & Monte Carlo Simulation Engine

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?logo=streamlit)]([YOUR_STREAMLIT_URL_HERE](https://ryanchen-financial-risk-model.streamlit.app))
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)

### Background
As a mechanical engineer I use simulation and probabilistic modeling to assess structural risk. This project applies the same thinking to financial portfolios. Using Monte Carlo simulation and statistical risk metrics to quantify downside exposure the way professional risk teams do at major financial institutions.

### Live Demo
Try the interactive dashboard here:
👉 [Financial Risk Analyzer](https://ryanchen-financial-risk-model.streamlit.app)

Enter any tickers, adjust portfolio weights, and run a full risk analysis 
including Monte Carlo simulation and historical stress testing in real time.

### Features
- Real market data via yfinance
- Log return calculation
- Annualized volatility
- Weighted Value at Risk (95% confidence)
- Sharpe Ratio
- Monte Carlo Simulation (10,000 paths)
- Historical Stress Testing (2008, COVID, 2022)

### Requirements
- Python 3.10+
- yfinance
- pandas
- numpy
- matplotlib

### Project Structure
````
financial-risk-model/
├── main.py
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── data_loader.py
│   ├── risk_metrics.py
│   ├── monte_carlo.py
│   └── stress_test.py
└── charts/
````

### Visualizations
![Monte Carlo Example](Charts/Monte_Carlo.png)
![Stress Test for 2008 Example](Charts/Stress_Test_2008.png)
![Stress Test for COVID Example](Charts/Stress_Test_COVID.png)
![Stress Test for 2022 Example](Charts/Stress_Test_2022.png)

### How to Run It

**Run the interactive dashboard:**
```bash
streamlit run app.py
```

**Run the command line analysis:**
```bash
git clone https://github.com/RyanChenEng/financial-risk-model
cd financial-risk-model
pip install -r requirements.txt
python3 main.py
```

### Key Concepts
- **Log Returns** - Measures daily price changes as ratios rather than raw differences making gains and losses symmetrical and consistent for modeling.
- **Volatility** - Annualized standard deviation of returns measuring how rapidly prices move (higher = more risk)
- **Value at Risk** - Maximum loss expected for 95% of days using historical losses
- **Sharpe Ratio** - Measures returns per unit of risk taken (higher = better)
- **Monte Carlo Simulation** - Simulates 10,000 possible portoflio futures based on historical average returns and volatility
- **Stress Test** - Simulates given portfolio during different economic crises

### What's Next?
- Streamlit dashboard for user inputs
- CVaR (Conditional Value at Risk)
- Portfolio optimization
- Additional crisis periods
