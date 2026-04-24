# Nike vs Lululemon Financial Analysis Dashboard

An interactive financial analysis tool comparing Nike and Lululemon across key profitability metrics (Gross Margin, Net Margin, ROA, ROE) and revenue trends from 2021 to 2025.

🔗 Live App: [https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/](https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/)

## 1. Problem & User
How have Nike and Lululemon performed financially over the past five years, and which company offers higher profitability for investors? This dashboard is designed for accounting students, retail investors, and financial analysts who want an interactive way to compare gross margin, net margin, return on assets (ROA), and return on equity (ROE) between two major sportswear companies.

## 2. Data
- **Source:** Nike and Lululemon annual reports (FY2021–FY2025)
- **URL:** Manually collected from company filings (SEC EDGAR / investor relations pages)
- **Accessed:** April 2026
- **Key fields:** revenue, cost, expenses, assets, liabilities
- **Metrics calculated:** gross margin, net margin, ROA, ROE
- **Period:** 2021–2025 (five fiscal years)
- **Unit:** Billion USD

## 3. Methods
- Data loading and cleaning using **pandas**
- Calculated financial metrics:
  - Gross Profit = Revenue – Cost
  - Gross Margin = (Revenue – Cost) / Revenue × 100
  - Net Profit = Gross Profit – Expenses
  - Net Margin = Net Profit / Revenue × 100
  - Equity = Assets – Liabilities
  - ROA = Net Profit / Assets × 100
  - ROE = Net Profit / Equity × 100
- Missing value handling: none – full data available for all years
- Interactive visualisation using **matplotlib** (bar charts, line charts, pie charts)
- Streamlit app with sidebar filters for year, analysis type (single year / multi‑year trend), and company selection
- Industry average benchmark comparison (45% gross margin, 12% net margin) for single‑year analysis
- Trend analysis for five‑year performance, including gross margin and revenue trends

## 4. Key Findings
- **Lululemon** consistently has higher gross margin (~60%) than Nike (~44%)
- Lululemon’s net margin (~27%) is more than double Nike’s (~11%)
- Lululemon’s ROE (~64%) significantly outperforms Nike (~25%), indicating stronger shareholder returns
- Nike’s 2025 revenue ($53.5B) is over 4× larger than Lululemon’s ($12.0B), demonstrating scale advantage
- Both companies exceed industry average gross margin (45%), with Lululemon far above
- Five‑year trend shows Lululemon’s margins remained stable while Nike’s slightly declined

## 5. How to Run

1. Make sure you have Python installed (version 3.8 or above).
2. Download the project files (`app.py`, `nike_lulu.csv`, `requirements.txt`) into a folder.
3. Open a terminal in that folder.
4. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
6. Product Link / Demo
🔗 Live App: https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/

7. Limitations & Next Steps
Limited company scope: Only Nike and Lululemon are compared; adding Adidas or Under Armour would give a broader industry view.
Data collection method: Manually extracted from annual reports; possible entry errors. Future versions could integrate live data via API (e.g., Yahoo Finance).
No causal inference: Correlations and comparisons are descriptive; no regression or panel modelling is performed.
Industry averages: The assumed industry averages (45% gross margin, 12% net margin) are approximations; actual industry numbers may vary.
Forecasting missing: No predictive model for future performance; linear trend lines could be added.
Fixed time period: Only five years (2021–2025) are included; longer historical data would provide more robust trend analysis.
Next steps: Add more competitors, implement automatic data refresh using financial APIs, add time‑series forecasting (e.g., ARIMA), and include additional ratios like operating margin or current ratio.
