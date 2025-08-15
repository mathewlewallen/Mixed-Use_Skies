#!/usr/bin/env python3
import numpy as np, pandas as pd
from pathlib import Path
rng = np.random.default_rng(42)
bins = [(0.00,0.25,0.15,0.12,500),(0.25,0.50,0.45,0.40,500),(0.50,0.75,0.70,0.66,500),(0.75,1.00,0.90,0.88,500)]
rows=[]
for lo,hi,conf,acc,cnt in bins:
    p = np.clip(rng.normal(conf,0.06,size=cnt), lo+1e-6, hi-1e-6)
    y = (rng.random(cnt) < acc).astype(int)
    rows.append(pd.DataFrame({"y_true":y,"y_prob":p}))
df = pd.concat(rows, ignore_index=True)
out = Path(__file__).resolve().parent / "preds.csv"
df.to_csv(out, index=False)
print(f"[OK] wrote {out} with shape {df.shape}")
