#!/usr/bin/env python3
import argparse, json, sys
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, shape
from shapely.ops import unary_union
import geopandas as gpd

def maybe_cartopy():
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        return ccrs, cfeature
    except Exception:
        return None, None

def load_tracks(path):
    try:
        gdf = gpd.read_file(path)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326")
        else:
            gdf = gdf.to_crs("EPSG:4326")
        gdf = gdf[gdf.geometry.type.isin(["LineString","MultiLineString"])]
        return gdf
    except Exception as e:
        print(f"[WARN] Could not load tracks: {e}", file=sys.stderr)
        return None

def main():
    ap = argparse.ArgumentParser(description="Make closure_example.png from hazard CSV and optional tracks GeoJSON")
    ap.add_argument("hazard_csv", help="CSV with columns lon,lat,order (WGS84)")
    ap.add_argument("outfile", help="Output PNG path")
    ap.add_argument("--tracks", help="GeoJSON of reroute polylines", default=None)
    ap.add_argument("--cartopy", action="store_true", help="Use cartopy basemap (requires cartopy installed)")
    ap.add_argument("--title", default="Static closure (NOTAM/LNM) and observed reroutes")
    args = ap.parse_args()

    df = pd.read_csv(args.hazard_csv).sort_values("order")
    poly = Polygon(list(zip(df["lon"], df["lat"])))
    gpoly = gpd.GeoSeries([poly], crs="EPSG:4326")

    tracks = load_tracks(args.tracks) if args.tracks else None

    if args.cartopy:
        ccrs, cfeature = maybe_cartopy()
        if ccrs is None:
            print("[WARN] cartopy not available, falling back to plain axes.", file=sys.stderr)
            args.cartopy = False

    if args.cartopy:
        fig = plt.figure(figsize=(7.2,5.6))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.LAND, facecolor="#f5f5f5")
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
        gpoly.boundary.plot(ax=ax, transform=ccrs.PlateCarree(), color="#dc2626", linewidth=1.6)
        if tracks is not None and len(tracks):
            tracks.plot(ax=ax, transform=ccrs.PlateCarree(), linewidth=0.6, color="#6b7280")
        ax.set_extent([df["lon"].min()-3, df["lon"].max()+3, df["lat"].min()-3, df["lat"].max()+3])
    else:
        fig, ax = plt.subplots(figsize=(7.2,5.6))
        x, y = gpoly.iloc[0].exterior.xy
        ax.plot(x, y, color="#dc2626", linewidth=1.6)
        if tracks is not None and len(tracks):
            te = tracks.explode(index_parts=False, ignore_index=True)
            for geom in te.geometry:
                if geom is None: continue
                if geom.geom_type == "LineString":
                    xs, ys = geom.xy
                    ax.plot(xs, ys, color="#6b7280", linewidth=0.6)
                elif geom.geom_type == "MultiLineString":
                    for ln in geom.geoms:
                        xs, ys = ln.xy
                        ax.plot(xs, ys, color="#6b7280", linewidth=0.6)
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_xlim(df["lon"].min()-0.5, df["lon"].max()+0.5)
        ax.set_ylim(df["lat"].min()-0.5, df["lat"].max()+0.5)
        ax.set_xlabel("Longitude"); ax.set_ylabel("Latitude")
    plt.title(args.title)
    plt.tight_layout()
    plt.savefig(args.outfile, dpi=300)
    print(f"[OK] Wrote {args.outfile}")

if __name__ == "__main__":
    main()
