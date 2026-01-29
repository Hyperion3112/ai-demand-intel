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
