"""Create a <=17,000-row subset from Kaggle Store Item Demand train.csv.
Usage: python src/prepare_kaggle_subset.py path/to/train.csv
Selects 8 complete store-item series (typically 8 * 1,826 = 14,608 rows).
"""
import sys
from pathlib import Path
import pandas as pd
if len(sys.argv)<2:
    raise SystemExit("Usage: python src/prepare_kaggle_subset.py path/to/train.csv")
src=Path(sys.argv[1]); df=pd.read_csv(src,parse_dates=["date"])
need={"date","store","item","sales"}
if not need.issubset(df.columns): raise SystemExit("Expected columns: date, store, item, sales")
counts=df.groupby(["store","item"]).size().sort_values(ascending=False)
chosen=list(counts[counts>=1800].head(8).index)
parts=[]
for store,item in chosen:
    g=df[(df.store==store)&(df.item==item)].sort_values("date")
    parts.append(g[["date","sales"]].assign(product_id=f"STORE_{store}_ITEM_{item}"))
out=pd.concat(parts,ignore_index=True)
if len(out)>17000: raise SystemExit(f"Subset has {len(out)} rows; reduce number of pairs")
out=out.rename(columns={"sales":"sales"})[["date","product_id","sales"]]
out.to_csv("data/real_sales_subset.csv",index=False)
print(f"Saved {len(out):,} rows to data/real_sales_subset.csv")
