## Live Dashboard
Tableau Public: https://public.tableau.com/views/AIDemandAdoptionIntelligenceUS/Dashboard1DemandCommandCenter?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

# AI Demand & Adoption Intelligence (US)

A market-intelligence analytics project that compares AI tools across categories (Image, Video, Coding) using real datasets to measure:
- Demand (search interest trends)
- Adoption (developer survey)
- Industry usage (enterprise report)
- Buzz / ecosystem momentum (optional)

## Dashboards (Tableau)
Planned dashboards:
1) Demand Command Center
2) Best Tool for the Job (Demand vs Confidence)
3) Industry Adoption Intelligence
4) Launch & Ecosystem Radar (optional)

## Data Sources (planned)
- Google Trends exports (US)
- Stack Overflow Developer Survey 2025
- McKinsey State of AI 2025
- (Optional) Product Hunt + GitHub repo metrics

## Repo Structure
- data/raw/         raw exports (not committed)
- data/processed/   cleaned datasets for Tableau
- etl/              scripts to pull/clean data
- tableau/          Tableau workbook + screenshots
- docs/             interview notes + executive summary

## Methodology (coming next)
We will compute:
- Demand Score (0–100): trends level + growth + momentum
- Confidence/Adoption Score (0–100): survey adoption (coding) + buzz/ecosystem (optional)

## Methodology (v1 — Demand Metrics)
We compute demand signals using Google Trends (US, last 12 months) for each tool keyword.

### Inputs
- `data/processed/tool_catalog.csv`
- `data/processed/trends_interest_over_time_us.csv`

### Metrics (per tool)
- **Demand Index (12m):** average Trends interest over the last 12 months
- **Current 4W Avg:** average interest over the most recent 28 days
- **Growth (Last 30 vs Previous 30):** percent change in average interest
- **Momentum (4W vs 12m):** percent change of recent 4-week average relative to 12-month average
- **Volatility:** standard deviation of weekly interest
- **Rank (overall and within category):** based on Demand Index (12m)

### Composite Score
- **Demand Score (0–100)** = normalized weighted mix:
  - 60% Demand Index (12m)
  - 25% Growth (Last 30 vs Previous 30)
  - 15% Momentum (4W vs 12m)

Output: `data/processed/tool_demand_metrics.csv`
