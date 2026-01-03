# Automated Company Analysis

This is a personal finance analysis project built for learning and experimentation.
It combines macroeconomic monitoring, market tracking, and automated company fundamental analysis into a single interactive Excel-based tool.

The goal is to provide a structured, data-driven framework to screen companies and understand market conditions efficiently.

## Main Features

### Macro Economic Analysis (US)
Provides a quick snapshot of the US economic environment using key indicators:
- 10Y US Treasury
- GDP Growth
- Unemployment Rate
- Inflation
- Fed Funds Rate

Data is fetched via the FRED API using a **Refresh Data** button (API key required in cell `G2`).
Each indicator is automatically scored (1–4), producing an overall macro classification from *Poor economy* to *Strong economy*.


### Markets
Tracks multiple global assets showing:
- Current price
- Daily % change
- Comparison vs. 52-week levels

Data is updated automatically using Yahoo Finance (yfinance).

### Company Analysis
The main sheet allows selecting from ~400 global companies.
When clicking **Search**, Excel calls a Python script located in the same folder, which:
- Fetches ~23 fundamental metrics from Yahoo Finance
- Ensures data consistency across the latest fiscal period
- Returns structured results to Excel

Metrics are compared against sector averages (benchmark calculated on December 7, 2025).
Scoring logic:
- Better than sector average: +1
- Worse than sector average: −1

Outputs:
- Overall Score: −19 to +19
- KPI Score: −10 to +10

Both scores are combined into a final recommendation:
**Buy hard / Buy / Hold / Sell / Sell hard**

## Technical Setup
- Excel `.xlsm` with VBA macros  
- Python 3  
- Python package:

- Python script must be in the same folder as the Excel file
- Execution via Windows CMD / WSL

> macOS compatibility has not been fully tested.

---

## Disclaimer
This project was created for educational and personal interest purposes only.
It does not constitute investment advice, and results may contain errors.

---

## Contact
- Email: ignasi.garcia.martin.e@gmail.com  
- LinkedIn: Ignasi Garcia I Martin
