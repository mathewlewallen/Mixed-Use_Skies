#!/usr/bin/env python3
import argparse, json, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.calibration import CalibrationDisplay
from sklearn.utils import column_or_1d

def ece(y_true, y_prob, bins=4):
    y_true = column_or_1d(y_true)
    y_prob = column_or_1d(y_prob)
    edges = np.linspace(0, 1, bins+1)
    e = 0.0; N = len(y_true)
    perbin = []
    for b in range(bins):
        idx = (y_prob >= edges[b]) & (y_prob < edges[b+1] if b < bins-1 else y_prob <= edges[b+1])
        n = int(idx.sum())
        if n == 0:
            perbin.append({"bin":[float(edges[b]), float(edges[b+1])],"n":0,"conf":None,"acc":None})
            continue
        conf = float(y_prob[idx].mean())
        acc = float(y_true[idx].mean())
        e += (n/N) * abs(acc - conf)
        perbin.append({"bin":[float(edges[b]), float(edges[b+1])],"n":n,"conf":conf,"acc":acc})
    return float(e), perbin

def main():
    ap = argparse.ArgumentParser(description="Make reliability plot and ECE report")
    ap.add_argument("preds_csv", help="CSV with columns: y_true (0/1), y_prob (0..1)")
    ap.add_argument("outfile", help="Output PNG path")
    ap.add_argument("--bins", type=int, default=4, help="ECE bins (default 4)")
    args = ap.parse_args()

    df = pd.read_csv(args.preds_csv)
    y, p = df["y_true"].to_numpy(), df["y_prob"].to_numpy()

    fig, ax = plt.subplots(figsize=(5,4))
    CalibrationDisplay.from_predictions(y, p, n_bins=10, strategy="uniform", ax=ax)
    ax.plot([0,1],[0,1], "--", linewidth=1)
    e, perbin = ece(y, p, bins=args.bins)
    ax.set_title(f"Reliability diagram (ECE={e:.3f}, {args.bins} bins)")
    plt.tight_layout(); plt.savefig(args.outfile, dpi=300)
    rep = {"ece": e, "bins": args.bins, "per_bin": perbin}
    with open("ece.json","w") as f:
        json.dump(rep, f, indent=2)
    print(f"[OK] Wrote {args.outfile} and ece.json")

if __name__ == "__main__":
    main()
