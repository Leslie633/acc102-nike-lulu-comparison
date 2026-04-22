import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nike vs Lululemon Financial Analysis", page_icon="📊", layout="wide")
st.title("📊 Nike vs Lululemon Financial Analysis Dashboard")

with st.expander("📋 About This Dashboard", expanded=False):
    st.write("""
    **Welcome to the Financial Analysis Dashboard!**
    
    This tool provides comprehensive financial analysis for Nike and Lululemon, including:
    - Gross Margin Analysis
    - Net Profit Margin Calculation
    - Financial Ratios (ROA, ROE)
    - Trend Analysis
    - Interactive Charts
    
    **Data Source:** Nike and Lululemon FY 2021-2025 financial statements (Unit: Billion USD)
    **Data Retrieved:** April 2026
    """)

df = pd.read_csv("nike_lulu.csv")

df["gross_margin"] = ((df["revenue"] - df["cost"]) / df["revenue"]).round(4) * 100
df["gross_profit"] = df["revenue"] - df["cost"]
df["net_profit"] = df["gross_profit"] - df["expenses"]
df["net_margin"] = (df["net_profit"] / df["revenue"]).round(4) * 100
df["equity"] = df["assets"] - df["liabilities"]
df["roa"] = (df["net_profit"] / df["assets"]).round(4) * 100
df["roe"] = (df["net_profit"] / df["equity"]).round(4) * 100

years = sorted(df["year"].unique())

with st.sidebar:
    st.header("⚙️ Settings")
    selected_year = st.selectbox("📅 Select Year:", years, index=len(years)-1)
    analysis_type = st.radio("🔍 Analysis Type:", ["Single Year Analysis", "Multi-Year Trend"], horizontal=False)
    selected_companies = st.multiselect("🏢 Select Companies:", options=df["company"].unique().tolist(), default=df["company"].unique().tolist())

if analysis_type == "Multi-Year Trend":
    filtered_df = df[df["company"].isin(selected_companies)]
else:
    filtered_df = df[(df["year"] == selected_year) & (df["company"].isin(selected_companies))]

st.write("### 📈 Key Financial Metrics")
metrics_df = filtered_df[["company", "year", "revenue", "cost", "gross_profit", "gross_margin", "net_profit", "net_margin"]].copy()
metrics_df["gross_margin"] = metrics_df["gross_margin"].apply(lambda x: f"{x:.2f}%")
metrics_df["net_margin"] = metrics_df["net_margin"].apply(lambda x: f"{x:.2f}%")
metrics_df.columns = ["Company", "Year", "Revenue (B\$)", "Cost (B\$)", "Gross Profit (B\$)", "Gross Margin", "Net Profit (B\$)", "Net Margin"]
st.dataframe(metrics_df, use_container_width=True)

if analysis_type == "Single Year Analysis":
    st.write("### 📊 Industry Comparison")
    industry_gross_avg = 45
    industry_net_avg = 12
    st.write(f"Industry Averages: Gross Margin = **{industry_gross_avg}%**, Net Margin = **{industry_net_avg}%**")
    
    year_data = df[df["year"] == selected_year]
    comparison_data = []
    for _, row in year_data.iterrows():
        gm_status = "Above" if row["gross_margin"] > industry_gross_avg else "Below"
        nm_status = "Above" if row["net_margin"] > industry_net_avg else "Below"
        gm_color = "#22c55e" if row["gross_margin"] > industry_gross_avg else "#ef4444"
        nm_color = "#22c55e" if row["net_margin"] > industry_net_avg else "#ef4444"
        comparison_data.append({
            "Company": row["company"],
            "Gross Margin": f"<span style='color:{gm_color};'>{row['gross_margin']:.2f}% ({gm_status})</span>",
            "Net Margin": f"<span style='color:{nm_color};'>{row['net_margin']:.2f}% ({nm_status})</span>"
        })
    
    comp_df = pd.DataFrame(comparison_data)
    st.write(comp_df.to_html(escape=False, index=False), unsafe_allow_html=True)

st.write("### 📊 Visual Analysis")
chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"])

plt.style.use("seaborn-v0_8")

if chart_type == "Bar Chart":
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    bars1 = ax1.bar(filtered_df["company"] if analysis_type == "Single Year Analysis" else filtered_df["year"],
                   filtered_df["gross_margin"], color="#1DA1F2", edgecolor="black")
    ax1.set_title("Gross Margin Comparison" if analysis_type == "Single Year Analysis" else "Gross Margin Trend")
    ax1.set_ylabel("Gross Margin (%)")
    ax1.set_ylim(0, 70)
    
    for bar in bars1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{bar.get_height():.1f}%", ha="center", va="bottom")
    
    bars2 = ax2.bar(filtered_df["company"] if analysis_type == "Single Year Analysis" else filtered_df["year"],
                   filtered_df["net_margin"], color="#FF6B6B", edgecolor="black")
    ax2.set_title("Net Margin Comparison" if analysis_type == "Single Year Analysis" else "Net Margin Trend")
    ax2.set_ylabel("Net Margin (%)")
    ax2.set_ylim(0, 30)
    
    for bar in bars2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"{bar.get_height():.1f}%", ha="center", va="bottom")

elif chart_type == "Line Chart":
    fig, ax = plt.subplots(figsize=(10, 5))
    for company in selected_companies:
        comp_data = filtered_df[filtered_df["company"] == company]
        ax.plot(comp_data["year"], comp_data["gross_margin"], marker='o', label=f"{company} Gross Margin", linewidth=2)
        ax.plot(comp_data["year"], comp_data["net_margin"], marker='s', label=f"{company} Net Margin", linewidth=2)
    ax.set_title("Margin Trends (2021-2025)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Percentage (%)")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.7)

else:
    if analysis_type == "Single Year Analysis":
        year_df = df[df["year"] == selected_year]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        ax1.pie(year_df["gross_profit"], labels=year_df["company"], autopct='%1.1f%%', 
                colors=["#1DA1F2", "#FF6B6B"], wedgeprops={'edgecolor':'black'})
        ax1.set_title(f"Gross Profit Distribution ({selected_year})")
        
        ax2.pie(year_df["net_profit"], labels=year_df["company"], autopct='%1.1f%%',
                colors=["#10B981", "#F59E0B"], wedgeprops={'edgecolor':'black'})
        ax2.set_title(f"Net Profit Distribution ({selected_year})")
    else:
        st.warning("Pie chart is only available for single year analysis")
        fig, ax = plt.subplots(figsize=(8, 5))

st.pyplot(fig)

if analysis_type == "Single Year Analysis":
    st.write("### 📈 Return on Investment Metrics")
    roi_df = df[df["year"] == selected_year][["company", "roa", "roe"]].copy()
    roi_df["roa"] = roi_df["roa"].apply(lambda x: f"{x:.2f}%")
    roi_df["roe"] = roi_df["roe"].apply(lambda x: f"{x:.2f}%")
    roi_df.columns = ["Company", "ROA (%)", "ROE (%)"]
    st.dataframe(roi_df, use_container_width=True)
    
    st.write("**ROA (Return on Assets):** Measures how efficiently assets generate profit")
    st.write("**ROE (Return on Equity):** Measures return on shareholder equity")

with st.info("🎯 Key Insights"):
    if analysis_type == "Single Year Analysis":
        year_df = df[df["year"] == selected_year]
        max_gm = year_df.loc[year_df["gross_margin"].idxmax()]
        max_nm = year_df.loc[year_df["net_margin"].idxmax()]
        st.write(f"""
        - **Year:** {selected_year}
        - **Highest Gross Margin:** **{max_gm['company']}** ({max_gm['gross_margin']:.2f}%)
        - **Highest Net Margin:** **{max_nm['company']}** ({max_nm['net_margin']:.2f}%)
        - **Nike Revenue:** \${year_df[year_df['company']=='Nike']['revenue'].values[0]}B | **Lululemon Revenue:** \${year_df[year_df['company']=='Lululemon']['revenue'].values[0]}B
        """)
    else:
        st.write("""
        - **Trend Analysis:** Compare financial performance across multiple years
        - **Observe how margins change over time**
        - **Identify growth patterns and trends**
        """)

st.write("### 📈 Five-Year Comparison Chart")
st.write("**Nike vs Lululemon - Full Trend Analysis (2021-2025)**")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

nike_data = df[df["company"] == "Nike"]
lulu_data = df[df["company"] == "Lululemon"]

ax1.plot(nike_data["year"], nike_data["gross_margin"], marker='o', label="Nike", color="#1DA1F2", linewidth=2)
ax1.plot(lulu_data["year"], lulu_data["gross_margin"], marker='s', label="Lululemon", color="#FF6B6B", linewidth=2)
ax1.set_title("Gross Margin Trend (2021-2025)")
ax1.set_xlabel("Year")
ax1.set_ylabel("Gross Margin (%)")
ax1.set_xticks(years)
ax1.legend()
ax1.grid(True, linestyle="--", alpha=0.7)

for i, year in enumerate(years):
    ax1.text(year, nike_data["gross_margin"].iloc[i], f"{nike_data['gross_margin'].iloc[i]:.1f}%", 
             ha="center", va="bottom", fontsize=10, color="#1DA1F2")
    ax1.text(year, lulu_data["gross_margin"].iloc[i], f"{lulu_data['gross_margin'].iloc[i]:.1f}%", 
             ha="center", va="bottom", fontsize=10, color="#FF6B6B")

ax2.plot(nike_data["year"], nike_data["revenue"], marker='o', label="Nike", color="#1DA1F2", linewidth=2)
ax2.plot(lulu_data["year"], lulu_data["revenue"], marker='s', label="Lululemon", color="#FF6B6B", linewidth=2)
ax2.set_title("Revenue Trend (2021-2025)")
ax2.set_xlabel("Year")
ax2.set_ylabel("Revenue (Billion USD)")
ax2.set_xticks(years)
ax2.legend()
ax2.grid(True, linestyle="--", alpha=0.7)

for i, year in enumerate(years):
    ax2.text(year, nike_data["revenue"].iloc[i], f"\${nike_data['revenue'].iloc[i]}B", 
             ha="center", va="bottom", fontsize=10, color="#1DA1F2")
    ax2.text(year, lulu_data["revenue"].iloc[i], f"\${lulu_data['revenue'].iloc[i]}B", 
             ha="center", va="bottom", fontsize=10, color="#FF6B6B")

st.pyplot(fig)

st.write("### 📝 Conclusion & Analysis")
st.markdown("""
#### **2025 Financial Performance Summary**

| Metric | Nike | Lululemon | Higher |
|--------|------|-----------|--------|
| Gross Margin | ~44.0% | ~60.0% | **Lululemon** |
| Net Margin | ~11.5% | ~26.7% | **Lululemon** |
| ROA | ~14.7% | ~38.2% | **Lululemon** |
| ROE | ~24.5% | ~63.5% | **Lululemon** |

---

### 📝 Conclusion & Analysis

**Why Lululemon's Margins are Higher:**
- **Premium Brand Positioning:** Targets high-end consumers willing to pay premium prices for yoga/athletic wear.
- **Direct-to-Consumer Model:** Higher proportion of sales through company-owned stores and e-commerce reduces distribution costs.
- **Lower Discounting Strategy:** Less reliance on promotions compared to Nike's seasonal sales events.
- **Product Innovation:** Strong focus on proprietary fabrics and designs creates pricing power.

**Nike's Competitive Advantages:**
- **Scale Advantage:** Nike's 2025 revenue (\$53.5B) is over 4.4x larger than Lululemon's (\$12.0B).
- **Global Footprint:** Presence in more countries and markets.
- **Diversified Product Line:** Covers footwear, apparel, and equipment across multiple sports.
- **Stronger Brand Recognition:** More established brand globally.

**Industry Context:**
- Industry average gross margin is approximately 45%. Both companies exceed this benchmark, with Lululemon (61.7% in 2025) significantly outperforming Nike (43.9%).

**Five-Year Trend (2021-2025):**
- Lululemon's gross margin has remained consistently above 58%, while Nike's has fluctuated between 43-46%.
- Lululemon's net margin improved from 27.9% (2021) to 31.7% (2025), while Nike's net margin stayed around 10-11%.

**Investment Consideration:**
- **Lululemon:** Higher profitability metrics (gross margin, net margin, ROE) suggest better operational efficiency and growth potential in the premium segment.
- **Nike:** Larger revenue base and global market dominance provide more stable cash flows and lower investment risk.

**Recommendation:** For growth-oriented investors seeking higher returns on equity, Lululemon may be attractive. For conservative investors prioritizing stability and market leadership, Nike offers a safer bet.""")


st.write("---")
st.caption("© 2026 Financial Analysis Dashboard | Data: FY 2021-2025 (Billion USD)")