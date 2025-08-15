#!/usr/bin/env python3
from graphviz import Digraph

g = Digraph("DRC", format="png")
g.attr(rankdir="LR", splines="ortho", nodesep="0.6", ranksep="0.7")
g.attr("node", shape="box", style="rounded,filled", fillcolor="#f3f4f6", color="#111827", penwidth="1.2", fontsize="12")

g.node("Ingest", "Ingest")
g.node("TIU", "TIU / UKF\n(P99 ≤ 0.5 s)")
g.node("ADHE", "ADHE\n(P99 ≤ 0.5 s)")
g.node("Poly", "Polygonize / Simplify\n(P99 ≤ 0.4 s)")
g.node("Pub", "Sign / Publish\n(P99 ≤ 0.3 s)")

g.edge("Ingest", "TIU", label="telemetry")
g.edge("TIU", "ADHE", label="state dist.")
g.edge("ADHE", "Poly", label="hazard field")
g.edge("Poly", "Pub", label="DRC slice")

with g.subgraph(name="cluster_ops") as c:
    c.attr(label="Monitors • Rollback • Immutable Replay", style="dashed", color="#6b7280", fontsize="11")
    c.node("L", "Liveness/Latency")
    c.node("C", "Calibration")
    c.node("K", "Containment")
    c.node("W", "Watchdog")

g.edge("Ingest", "L", style="dotted", color="#6b7280")
g.edge("TIU", "C", style="dotted", color="#6b7280")
g.edge("Poly", "K", style="dotted", color="#6b7280")
g.edge("Pub", "W", style="dotted", color="#6b7280")

g.render("blockdiag", cleanup=True)
print("[OK] Wrote blockdiag.png")
