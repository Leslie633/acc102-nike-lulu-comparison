import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Nike vs Lululemon Financial Analysis", page_icon="📊", layout="wide")

# Custom CSS 
st.markdown("""
<style>
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f0f4f8;
        padding: 6px 10px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
    }
    /* Clean dataframe index removal */
    .dataframe-container { margin-top: 8px; }
</style>
""", unsafe_allow_html=True)

# Header 
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

# Load & Compute Data 
df = pd.read_csv("nike_lulu.csv")

df["gross_margin"] = ((df["revenue"] - df["cost"]) / df["revenue"]).round(4) * 100
df["gross_profit"] = df["revenue"] - df["cost"]
df["net_profit"]   = df["gross_profit"] - df["expenses"]
df["net_margin"]   = (df["net_profit"] / df["revenue"]).round(4) * 100
df["equity"]       = df["assets"] - df["liabilities"]
df["roa"]          = (df["net_profit"] / df["assets"]).round(4) * 100
df["roe"]          = (df["net_profit"] / df["equity"]).round(4) * 100

years = sorted(df["year"].unique())

# Sidebar 
with st.sidebar:
    st.header("⚙️ Settings")
    selected_year      = st.selectbox("📅 Select Year:", years, index=len(years) - 1)
    analysis_type      = st.radio("🔍 Analysis Type:", ["Single Year Analysis", "Multi-Year Trend"])
    selected_companies = st.multiselect(
        "🏢 Select Companies:",
        options=df["company"].unique().tolist(),
        default=df["company"].unique().tolist(),
    )

# Filtered data
if analysis_type == "Multi-Year Trend":
    filtered_df = df[df["company"].isin(selected_companies)]
else:
    filtered_df = df[(df["year"] == selected_year) & (df["company"].isin(selected_companies))]

# Tabs 
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Key Metrics",
    "📊 Visual Analysis",
    "💹 ROI Metrics",
    "📝 Conclusion",
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 · Key Metrics
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Key Financial Metrics")

    metrics_df = filtered_df[[
        "company", "year", "revenue", "cost",
        "gross_profit", "gross_margin", "net_profit", "net_margin"
    ]].copy().reset_index(drop=True)

    # Format percentage columns AFTER resetting index so row numbers are 1-based
    display_df = metrics_df.copy()
    display_df.index = range(1, len(display_df) + 1)          # 1-based index
    display_df["gross_margin"] = display_df["gross_margin"].apply(lambda x: f"{x:.2f}%")
    display_df["net_margin"]   = display_df["net_margin"].apply(lambda x: f"{x:.2f}%")
    display_df.columns = [
        "Company", "Year", "Revenue (B$)", "Cost (B$)",
        "Gross Profit (B$)", "Gross Margin", "Net Profit (B$)", "Net Margin"
    ]
    st.dataframe(display_df, use_container_width=True)

    # Industry comparison (single-year only) 
    if analysis_type == "Single Year Analysis":
        st.divider()
        st.subheader("Industry Comparison")

        industry_gross_avg = 45
        industry_net_avg   = 12
        st.write(f"Industry Averages: Gross Margin = **{industry_gross_avg}%**, Net Margin = **{industry_net_avg}%**")

        year_data       = df[df["year"] == selected_year]
        comparison_data = []
        for _, row in year_data.iterrows():
            gm_status = "Above" if row["gross_margin"] > industry_gross_avg else "Below"
            nm_status = "Above" if row["net_margin"]   > industry_net_avg   else "Below"
            gm_color  = "#22c55e" if row["gross_margin"] > industry_gross_avg else "#ef4444"
            nm_color  = "#22c55e" if row["net_margin"]   > industry_net_avg   else "#ef4444"
            comparison_data.append({
                "Company":     row["company"],
                "Gross Margin": f"<span style='color:{gm_color};font-weight:600'>{row['gross_margin']:.2f}% ({gm_status})</span>",
                "Net Margin":   f"<span style='color:{nm_color};font-weight:600'>{row['net_margin']:.2f}% ({nm_status})</span>",
            })

        comp_df = pd.DataFrame(comparison_data)
        st.write(comp_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # 5-year trend charts (always visible) 
    st.divider()
    st.subheader("Five-Year Comparison (2021-2025)")

    plt.style.use("seaborn-v0_8")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    nike_data = df[df["company"] == "Nike"]
    lulu_data = df[df["company"] == "Lululemon"]

    ax1.plot(nike_data["year"], nike_data["gross_margin"], marker='o', label="Nike",       color="#1DA1F2", linewidth=2)
    ax1.plot(lulu_data["year"], lulu_data["gross_margin"], marker='s', label="Lululemon",  color="#FF6B6B", linewidth=2)
    ax1.set_title("Gross Margin Trend (2021-2025)")
    ax1.set_xlabel("Year"); ax1.set_ylabel("Gross Margin (%)")
    ax1.set_xticks(years); ax1.legend(); ax1.grid(True, linestyle="--", alpha=0.7)
    for i, year in enumerate(years):
        ax1.text(year, nike_data["gross_margin"].iloc[i], f"{nike_data['gross_margin'].iloc[i]:.1f}%",
                 ha="center", va="bottom", fontsize=9, color="#1DA1F2")
        ax1.text(year, lulu_data["gross_margin"].iloc[i], f"{lulu_data['gross_margin'].iloc[i]:.1f}%",
                 ha="center", va="bottom", fontsize=9, color="#FF6B6B")

    ax2.plot(nike_data["year"], nike_data["revenue"], marker='o', label="Nike",      color="#1DA1F2", linewidth=2)
    ax2.plot(lulu_data["year"], lulu_data["revenue"], marker='s', label="Lululemon", color="#FF6B6B", linewidth=2)
    ax2.set_title("Revenue Trend (2021-2025)")
    ax2.set_xlabel("Year"); ax2.set_ylabel("Revenue (Billion USD)")
    ax2.set_xticks(years); ax2.legend(); ax2.grid(True, linestyle="--", alpha=0.7)
    for i, year in enumerate(years):
        ax2.text(year, nike_data["revenue"].iloc[i], f"${nike_data['revenue'].iloc[i]}B",
                 ha="center", va="bottom", fontsize=9, color="#1DA1F2")
        ax2.text(year, lulu_data["revenue"].iloc[i], f"${lulu_data['revenue'].iloc[i]}B",
                 ha="center", va="bottom", fontsize=9, color="#FF6B6B")

    st.pyplot(fig)
    plt.close(fig)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 · Visual Analysis
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Visual Analysis")
    chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"])

    plt.style.use("seaborn-v0_8")

    if chart_type == "Bar Chart":
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        x_vals  = filtered_df["company"] if analysis_type == "Single Year Analysis" else filtered_df["year"]
        title_s = "Comparison" if analysis_type == "Single Year Analysis" else "Trend"

        bars1 = ax1.bar(x_vals, filtered_df["gross_margin"], color="#1DA1F2", edgecolor="black")
        ax1.set_title(f"Gross Margin {title_s}")
        ax1.set_ylabel("Gross Margin (%)"); ax1.set_ylim(0, 70)
        for bar in bars1:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                     f"{bar.get_height():.1f}%", ha="center", va="bottom")

        bars2 = ax2.bar(x_vals, filtered_df["net_margin"], color="#FF6B6B", edgecolor="black")
        ax2.set_title(f"Net Margin {title_s}")
        ax2.set_ylabel("Net Margin (%)"); ax2.set_ylim(0, 30)
        for bar in bars2:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                     f"{bar.get_height():.1f}%", ha="center", va="bottom")

    elif chart_type == "Line Chart":
        fig, ax = plt.subplots(figsize=(10, 5))
        for company in selected_companies:
            comp_data = filtered_df[filtered_df["company"] == company]
            ax.plot(comp_data["year"], comp_data["gross_margin"], marker='o',
                    label=f"{company} Gross Margin", linewidth=2)
            ax.plot(comp_data["year"], comp_data["net_margin"], marker='s',
                    label=f"{company} Net Margin", linewidth=2)
        ax.set_title("Margin Trends (2021-2025)")
        ax.set_xlabel("Year"); ax.set_ylabel("Percentage (%)")
        ax.legend(); ax.grid(True, linestyle="--", alpha=0.7)

    else:  # Pie Chart
        if analysis_type == "Single Year Analysis":
            year_df = df[df["year"] == selected_year]
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            ax1.pie(year_df["gross_profit"], labels=year_df["company"], autopct='%1.1f%%',
                    colors=["#1DA1F2", "#FF6B6B"], wedgeprops={'edgecolor': 'black'})
            ax1.set_title(f"Gross Profit Distribution ({selected_year})")
            ax2.pie(year_df["net_profit"], labels=year_df["company"], autopct='%1.1f%%',
                    colors=["#10B981", "#F59E0B"], wedgeprops={'edgecolor': 'black'})
            ax2.set_title(f"Net Profit Distribution ({selected_year})")
        else:
            st.warning("Pie chart is only available for Single Year Analysis.")
            fig, ax = plt.subplots(figsize=(8, 5))

    st.pyplot(fig)
    plt.close(fig)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 · ROI Metrics
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Return on Investment Metrics")

    if analysis_type == "Single Year Analysis":
        roi_df = df[df["year"] == selected_year][["company", "roa", "roe"]].copy().reset_index(drop=True)
        roi_df.index = range(1, len(roi_df) + 1)          # 1-based index
        roi_df["roa"] = roi_df["roa"].apply(lambda x: f"{x:.2f}%")
        roi_df["roe"] = roi_df["roe"].apply(lambda x: f"{x:.2f}%")
        roi_df.columns = ["Company", "ROA (%)", "ROE (%)"]
        st.dataframe(roi_df, use_container_width=True)
    else:
        # Show all years
        roi_all = df[df["company"].isin(selected_companies)][["company", "year", "roa", "roe"]].copy().reset_index(drop=True)
        roi_all.index = range(1, len(roi_all) + 1)
        roi_all["roa"] = roi_all["roa"].apply(lambda x: f"{x:.2f}%")
        roi_all["roe"] = roi_all["roe"].apply(lambda x: f"{x:.2f}%")
        roi_all.columns = ["Company", "Year", "ROA (%)", "ROE (%)"]
        st.dataframe(roi_all, use_container_width=True)

    st.info("""
    **ROA (Return on Assets):** Measures how efficiently assets generate profit.  
    **ROE (Return on Equity):** Measures return on shareholder equity.
    """)

    # Key insights block
    st.divider()
    st.subheader("🎯 Key Insights")
    if analysis_type == "Single Year Analysis":
        year_df = df[df["year"] == selected_year]
        max_gm  = year_df.loc[year_df["gross_margin"].idxmax()]
        max_nm  = year_df.loc[year_df["net_margin"].idxmax()]
        nike_rev = year_df[year_df['company'] == 'Nike']['revenue'].values[0]
        lulu_rev = year_df[year_df['company'] == 'Lululemon']['revenue'].values[0]
        st.markdown(f"""
- **Year:** {selected_year}
- **Highest Gross Margin:** **{max_gm['company']}** ({max_gm['gross_margin']:.2f}%)
- **Highest Net Margin:** **{max_nm['company']}** ({max_nm['net_margin']:.2f}%)
- **Nike Revenue:** ${nike_rev}B &nbsp;|&nbsp; **Lululemon Revenue:** ${lulu_rev}B
        """)
    else:
        st.markdown("""
- **Trend Analysis:** Compare financial performance across multiple years
- **Observe how margins change over time**
- **Identify growth patterns and trends**
        """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 · Conclusion
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("2025 Financial Performance Summary")

    st.markdown("""
| Metric | Nike | Lululemon | Higher |
|--------|------|-----------|--------|
| Gross Margin | ~44.0% | ~60.0% | **Lululemon** |
| Net Margin | ~11.5% | ~26.7% | **Lululemon** |
| ROA | ~14.7% | ~38.2% | **Lululemon** |
| ROE | ~24.5% | ~63.5% | **Lululemon** |
    """)

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🏃 Why Lululemon's Margins are Higher")
        st.markdown("""
- **Premium Brand Positioning:** Targets high-end consumers willing to pay premium prices for yoga/athletic wear.
- **Direct-to-Consumer Model:** Higher proportion of sales through company-owned stores and e-commerce reduces distribution costs.
- **Lower Discounting Strategy:** Less reliance on promotions compared to Nike's seasonal sales events.
- **Product Innovation:** Strong focus on proprietary fabrics and designs creates pricing power.
        """)

    with col_b:
        st.markdown("#### ✔️ Nike's Competitive Advantages")
        st.markdown("""
- **Scale Advantage:** Nike's 2025 revenue ($53.5B) is over 4.4× larger than Lululemon's ($12.0B).
- **Global Footprint:** Presence in more countries and markets.
- **Diversified Product Line:** Covers footwear, apparel, and equipment across multiple sports.
- **Stronger Brand Recognition:** More established brand globally.
        """)

    st.divider()
    st.markdown("#### 📈 Industry Context & Five-Year Trend")
    st.markdown("""
- Industry average gross margin is approximately **45%**. Both companies exceed this benchmark, with Lululemon (61.7% in 2025) significantly outperforming Nike (43.9%).
- Lululemon's gross margin has remained consistently **above 58%**, while Nike's has fluctuated between 43–46%.
- Lululemon's net margin improved from 27.9% (2021) to 31.7% (2025), while Nike's net margin stayed around 10–11%.
    """)

    st.divider()
    st.markdown("#### 💼 Investment Consideration")
    col_c, col_d = st.columns(2)
    with col_c:
        st.info("**Lululemon:** Higher profitability metrics (gross margin, net margin, ROE) suggest better operational efficiency and growth potential in the premium segment. Suited for **growth-oriented investors**.")
    with col_d:
        st.info("**Nike:** Larger revenue base and global market dominance provide more stable cash flows and lower investment risk. Suited for **conservative investors** prioritizing stability.")

# Footer 
st.write("---")
st.caption("© 2026 Financial Analysis Dashboard | Data: FY 2021-2025 (Billion USD)")
