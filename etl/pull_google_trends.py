import time
import pandas as pd
from pytrends.request import TrendReq

TOOLS_CSV = "data/processed/tool_catalog.csv"
OUT_CSV = "data/processed/trends_interest_over_time_us.csv"

def fetch_interest_over_time(pytrends: TrendReq, keyword: str) -> pd.DataFrame:
    """
    Fetch interest over time for a single keyword in the US for the last 12 months.
    Output columns: date, keyword, interest_index, geo, timeframe
    """
    pytrends.build_payload([keyword], timeframe="today 12-m", geo="US")
    df = pytrends.interest_over_time()

    if df is None or df.empty:
        return pd.DataFrame(columns=["date", "keyword", "interest_index", "geo", "timeframe"])

    df = df.reset_index()
    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    df = df.rename(columns={keyword: "interest_index"})
    df["keyword"] = keyword
    df["geo"] = "US"
    df["timeframe"] = "today 12-m"

    return df[["date", "keyword", "interest_index", "geo", "timeframe"]]

def main():
    tools = pd.read_csv(TOOLS_CSV)
    keywords = tools["trend_keyword"].dropna().unique().tolist()

    pytrends = TrendReq(hl="en-US", tz=360)

    frames = []
    for i, kw in enumerate(keywords, start=1):
        print(f"[{i}/{len(keywords)}] Fetching: {kw}")
        try:
            frames.append(fetch_interest_over_time(pytrends, kw))
        except Exception as e:
            print(f"  !! Error for {kw}: {e}")

        # Avoid rate limiting
        time.sleep(2)

    out = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    out.to_csv(OUT_CSV, index=False)
    print(f"\nSaved: {OUT_CSV} | rows={len(out)}")

if __name__ == "__main__":
    main()
