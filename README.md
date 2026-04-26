# Nike vs Lululemon Financial Analysis Dashboard

An interactive financial analysis tool comparing Nike and Lululemon across key profitability metrics (Gross Margin, Net Margin, ROA, ROE) and revenue trends from 2021 to 2025.

🔗 Live App: [https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/](https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/)

## 1. Problem & User
How have Nike and Lululemon performed financially over the past five years, and which company offers higher profitability for investors? This dashboard is designed for accounting students, retail investors, and financial analysts who want an interactive way to compare gross margin, net margin, return on assets (ROA), and return on equity (ROE) between two major sportswear companies.

## 2. Data
- **Source:** Nike and Lululemon annual reports (Form 10-K) filed with the U.S. Securities and Exchange Commission (SEC), FY2021–FY2025.
- **Accessed:** April 25 2026
- **Key fields:** revenue, cost, expenses, assets, liabilities
- **Metrics calculated:** gross margin, net margin, ROA, ROE
- **Period:** 2021–2025
- **Unit:** Billion USD

## 3. Methods
The dashboard is built using **Streamlit** for the interactive web interface, **pandas** for data manipulation, and **matplotlib** for plotting.

**Data processing steps:**
- Load CSV and compute gross margin, net margin, ROA, ROE.
- Reshape data for multi-year trend analysis.

**Interactive features (sidebar):**
- **Year selector:** Users can pick a specific fiscal year (2021–2025) for single‑year analysis.
- **Analysis type toggle:** Switch between “Single Year Analysis” (static comparison) and “Multi‑Year Trend” (time‑series view).
- **Company multiselect:** Choose one or both companies (Nike, Lululemon) to compare.

**Outputs:**
- Tabbed layout: Key Metrics (tables + industry benchmarks), Visual Analysis (bar/pie/line charts), ROI Metrics (ROA/ROE), Conclusion.
- Dynamic chart type adapts to analysis type: pie chart only for single year, line chart only for multi‑year.
- Industry comparison (gross margin 45%, net margin 12%) highlights under/over performance.

## 4. Key Findings
- **Lululemon** consistently has higher gross margin (~60%) than Nike (~44%)
- Lululemon’s net margin (~27%) is more than double Nike’s (~11%)
- Lululemon’s ROE (~64%) significantly outperforms Nike (~25%), indicating stronger shareholder returns
- Nike’s 2025 revenue ($53.5B) is over 4× larger than Lululemon’s ($12.0B), demonstrating scale advantage
- Both companies exceed industry average gross margin (45%), with Lululemon far above
- Five‑year trend shows Lululemon’s margins remained stable while Nike’s slightly declined

## 5. How to Run

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
2. Run the app:
   ```bash
   python -m streamlit run app.py

## 6. Product Link
🔗 Live App:[https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/](https://acc102-nike-lulu-comparison-43dfjfrpcvmxk48dcja8ap.streamlit.app/)

## 7. Limitations & Next Steps
- **Limited company scope:** Only Nike and Lululemon are compared; adding Adidas or Under Armour would give a broader industry view.
- **Short time horizon** – The analysis covers only five fiscal years (2021–2025). A longer time series (10+ years) could reveal more reliable long‑term trends and cyclical patterns.
- **No real‑time or forecast ability** – The dashboard reflects historical data only. Adding a simple linear regression or time‑series forecast would help users anticipate future margins.
- **Simplified industry benchmark** – The 45% gross / 12% net margin benchmarks are fixed estimates. Making them user‑adjustable (via sidebar sliders) would improve customisation.
- **Missing financial metrics** – Metrics like free cash flow, debt‑to‑equity, or inventory turnover are not included. Adding them would enable deeper financial health analysis.
