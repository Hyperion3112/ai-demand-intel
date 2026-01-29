import pandas as pd
import numpy as np

TOOLS_CSV = "data/processed/tool_catalog.csv"
TRENDS_CSV = "data/processed/trends_interest_over_time_us.csv"
OUT_CSV = "data/processed/tool_demand_metrics.csv"

def safe_pct_change(new, old):
    if old == 0 or pd.isna(old) or pd.isna(new):
        return np.nan
    return (new - old) / old * 100.0

def main():
    tools = pd.read_csv(TOOLS_CSV)
    trends = pd.read_csv(TRENDS_CSV, parse_dates=["date"])

    # Join tool metadata onto trends by keyword
    df = trends.merge(
        tools,
        left_on="keyword",
        right_on="trend_keyword",
        how="left"
    )

    # Sanity: drop rows without tool mapping
    df = df.dropna(subset=["tool", "category"])

    # Determine “current” date in the dataset
    max_date = df["date"].max()

    # Define windows
    last_4w_start = max_date - pd.Timedelta(days=28)
    last_30d_start = max_date - pd.Timedelta(days=30)
    prev_30d_start = max_date - pd.Timedelta(days=60)

    metrics = []

    for tool_name, g in df.groupby("tool"):
        category = g["category"].iloc[0]
        company = g["company"].iloc[0]
        kw = g["keyword"].iloc[0]

        # 12-month baseline
        demand_12m = g["interest_index"].mean()
        volatility = g["interest_index"].std()

        # Current 4 weeks
        g_4w = g[g["date"] >= last_4w_start]
        current_4w_avg = g_4w["interest_index"].mean() if not g_4w.empty else np.nan

        # Growth: last 30 days vs prior 30 days
        last_30 = g[g["date"] >= last_30d_start]["interest_index"].mean()
        prev_30 = g[(g["date"] >= prev_30d_start) & (g["date"] < last_30d_start)]["interest_index"].mean()
        growth_90d = safe_pct_change(last_30, prev_30)

        # Momentum: current 4w avg relative to 12m avg
        momentum_4w = safe_pct_change(current_4w_avg, demand_12m)

        metrics.append({
            "tool": tool_name,
            "company": company,
            "category": category,
            "trend_keyword": kw,
            "max_date_in_data": max_date.date().isoformat(),
            "demand_index_12m": round(demand_12m, 2),
            "current_4w_avg": round(current_4w_avg, 2) if pd.notna(current_4w_avg) else np.nan,
            "growth_last30_vs_prev30_pct": round(growth_90d, 2) if pd.notna(growth_90d) else np.nan,
            "momentum_4w_vs_12m_pct": round(momentum_4w, 2) if pd.notna(momentum_4w) else np.nan,
            "volatility_std": round(volatility, 2) if pd.notna(volatility) else np.nan,
        })

    out = pd.DataFrame(metrics)

    # Overall rank by 12m demand
    out["rank_overall_by_demand_12m"] = out["demand_index_12m"].rank(ascending=False, method="min").astype(int)

    # Category rank by 12m demand
    out["rank_in_category_by_demand_12m"] = out.groupby("category")["demand_index_12m"] \
        .rank(ascending=False, method="min").astype(int)

    # Simple “Demand Score” 0–100 using normalized mix
    # demand_index_12m (60%), growth (25%), momentum (15%)
    def minmax(s):
        if s.nunique() <= 1:
            return pd.Series([50]*len(s), index=s.index)
        return (s - s.min()) / (s.max() - s.min()) * 100

    demand_norm = minmax(out["demand_index_12m"])
    growth_norm = minmax(out["growth_last30_vs_prev30_pct"].fillna(out["growth_last30_vs_prev30_pct"].median()))
    mom_norm = minmax(out["momentum_4w_vs_12m_pct"].fillna(out["momentum_4w_vs_12m_pct"].median()))

    out["demand_score_0_100"] = (0.60 * demand_norm + 0.25 * growth_norm + 0.15 * mom_norm).round(2)

    out = out.sort_values(["category", "rank_in_category_by_demand_12m", "tool"])
    out.to_csv(OUT_CSV, index=False)
    print(f"Saved: {OUT_CSV} | rows={len(out)}")

if __name__ == "__main__":
    main()
