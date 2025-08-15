#!/usr/bin/env python3
# Usage:
#   python make_closure_example.py hazard.csv closure_example.png [--tracks tracks.geojson]
import argparse, csv, json, math, pathlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs, cartopy.feature as cfeature
from shapely.geometry import Polygon

def read_hazard_csv(path):
    pts = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            pts.append((float(row["lon"]), float(row["lat"])))
    return pts

def read_tracks_geojson(path):
    with open(path) as f:
        gj = json.load(f)
    lines = []
    for feat in gj.get("features", []):
        geom = feat.get("geometry", {})
        if geom.get("type") == "LineString":
            lines.append(geom.get("coordinates", []))
    return lines

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("hazard_csv")
    ap.add_argument("outfile")
    ap.add_argument("--tracks", help="FeatureCollection of LineString flight tracks (GeoJSON)")
    args = ap.parse_args()

    pts = read_hazard_csv(args.hazard_csv)
    poly = Polygon(pts)

    fig = plt.figure(figsize=(7.2, 5.6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND, facecolor="#f5f5f5")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6)
    # hazard boundary
    xs, ys = zip(*(list(poly.exterior.coords)))
    ax.plot(xs, ys, "-", linewidth=1.6, color="#dc2626", transform=ccrs.PlateCarree(), label="Hazard polygon")

    # optional tracks
    if args.tracks:
        for coords in read_tracks_geojson(args.tracks):
            if not coords: 
                continue
            tx, ty = zip(*coords)
            ax.plot(tx, ty, linewidth=0.6, color="#6b7280", alpha=0.9, transform=ccrs.PlateCarree())

    minx, miny, maxx, maxy = poly.bounds
    padx = max(1.5, (maxx - minx) * 0.1)
    pady = max(1.0, (maxy - miny) * 0.1)
    ax.set_extent([minx - padx, maxx + padx, miny - pady, maxy + pady], crs=ccrs.PlateCarree())

    ax.set_title("Static closure (official polygon) and reroutes (optional)")
    plt.tight_layout()
    pathlib.Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.outfile, dpi=300)
    print(f"[OK] Wrote {args.outfile}")
