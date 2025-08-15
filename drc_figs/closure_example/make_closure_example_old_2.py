#!/usr/bin/env python3
import argparse, csv, json, sys
from pathlib import Path
import matplotlib.pyplot as plt

def read_polygon_csv(csv_path):
    pts = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            pts.append((float(row["lon"]), float(row["lat"]), int(row["order"])))
    pts = sorted(pts, key=lambda t: t[2])
    xy = [(lon, lat) for lon, lat, _ in pts]
    if xy[0] != xy[-1]:
        xy.append(xy[0])
    return xy

def read_tracks_geojson(geojson_path):
    with open(geojson_path) as f:
        fc = json.load(f)
    lines = []
    for feat in fc.get("features", []):
        geom = feat.get("geometry", {})
        if geom.get("type") == "LineString":
            lines.append(geom["coordinates"]) 
    return lines

def main():
    p = argparse.ArgumentParser()
    p.add_argument("hazard_csv")
    p.add_argument("outfile")
    p.add_argument("--tracks", help="GeoJSON FeatureCollection of LineStrings", default=None)
    p.add_argument("--cartopy", action="store_true", help="draw coastlines (requires cartopy)")
    args = p.parse_args()

    ring = read_polygon_csv(args.hazard_csv)
    lons = [x for x,_ in ring]; lats = [y for _,y in ring]

    if args.cartopy:
        try:
            import cartopy.crs as ccrs, cartopy.feature as cfeature
            proj = ccrs.PlateCarree()
            fig = plt.figure(figsize=(7.2, 5.6))
            ax = plt.axes(projection=proj)
            ax.add_feature(cfeature.LAND, facecolor="#f5f5f5")
            ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
            ax.plot(lons, lats, "-", color="#dc2626", linewidth=1.6, transform=proj, zorder=5)
            if args.tracks:
                for line in read_tracks_geojson(args.tracks):
                    xs = [p[0] for p in line]; ys = [p[1] for p in line]
                    ax.plot(xs, ys, "-", linewidth=0.6, color="#6b7280", alpha=0.9, transform=proj, zorder=3)
            pad = 2
            ax.set_extent([min(lons)-pad, max(lons)+pad, min(lats)-pad, max(lats)+pad], crs=proj)
        except Exception as e:
            print(f"[warn] cartopy failed ({e}); falling back to plain Matplotlib.")
            args.cartopy = False

    if not args.cartopy:
        fig, ax = plt.subplots(figsize=(7.2, 5.6))
        ax.plot(lons, lats, "-", color="#dc2626", linewidth=1.6, zorder=5)
        if args.tracks:
            for line in read_tracks_geojson(args.tracks):
                xs = [p[0] for p in line]; ys = [p[1] for p in line]
                ax.plot(xs, ys, "-", linewidth=0.6, color="#6b7280", alpha=0.9, zorder=3)
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
        ax.grid(alpha=0.3)

    Path(args.outfile).parent.mkdir(parents=True, exist_ok=True)
    plt.title("Static closure (official polygon) and observed reroutes")
    plt.tight_layout(); plt.savefig(args.outfile, dpi=300)
    print(f"[OK] Wrote {args.outfile}")

if __name__ == "__main__":
    sys.exit(main())
