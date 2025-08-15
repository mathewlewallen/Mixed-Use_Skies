#!/usr/bin/env python3
import argparse
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def draw(poly, style, label=None):
    if poly.is_empty: return
    if hasattr(poly, "geoms"):
        for g in poly.geoms:
            x,y = g.exterior.xy; plt.plot(x,y, **style, label=label); label=None
    else:
        x,y = poly.exterior.xy; plt.plot(x,y, **style, label=label)

def main():
    ap = argparse.ArgumentParser(description="Containment demo: inward offset + ε-bounded simplification")
    ap.add_argument("--eps", type=float, default=0.20, help="epsilon (same units as local coords)")
    ap.add_argument("--outfile", default="containment_demo.png", help="output PNG path")
    args = ap.parse_args()

    outer = [(0,0),(7,0),(7,1.5),(4,1.5),(4,3.5),(7,3.5),(7,7),(0,7)]
    hole  = [(2,2),(2,5),(5,5),(5,2)]
    P = Polygon(outer, [hole])

    P_minus = P.buffer(-args.eps, join_style=2, mitre_limit=2.0)  # inward offset
    S = P_minus.simplify(args.eps, preserve_topology=True)        # topology-preserving DP

    plt.figure(figsize=(5,5))
    draw(P, {"color":"#2563eb","linestyle":"--","linewidth":1.5}, "P (true)")
    draw(P_minus, {"color":"#16a34a","linestyle":":","linewidth":1.5}, "P⊖Bε (inward)")
    draw(S, {"color":"#dc2626","linestyle":"-","linewidth":2.0}, "S (published)")
    plt.axis("equal"); plt.xticks([]); plt.yticks([])
    plt.legend(loc="lower right")
    plt.title("Containment via inward offset and ε-bounded simplification")
    plt.tight_layout(); plt.savefig(args.outfile, dpi=300)
    print(f"[OK] Wrote {args.outfile}")

if __name__ == "__main__":
    main()
