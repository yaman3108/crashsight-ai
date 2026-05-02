"""
CrashSight AI — Satellite Imagery Downloader

Downloads Sentinel-2 satellite tiles centered on known crash site coordinates.
Uses Microsoft Planetary Computer (free, no API key required).

Usage:
    python -m src.dataset.downloader                          # Download all seed sites
    python -m src.dataset.downloader --class PLANE_FOREST     # Download one class only
    python -m src.dataset.downloader --limit 5                # Download first 5 sites
    python -m src.dataset.downloader --output data/raw/       # Custom output directory

Data source: Sentinel-2 L2A via Microsoft Planetary Computer STAC API
Resolution: 10m/pixel (Bands 2,3,4 = Blue, Green, Red)
Tile size: 512x512 pixels = ~5.12km x 5.12km ground coverage
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import requests
from PIL import Image

# Microsoft Planetary Computer STAC API (free, no auth)
STAC_API_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Sentinel-2 band URLs use this pattern
TILE_SIZE = 512          # pixels
GSD = 10                 # meters/pixel (Sentinel-2 Band 4,3,2)
HALF_EXTENT = (TILE_SIZE * GSD) / 2  # meters from center (~2560m)


def load_seed_sites(csv_path: str, class_filter: str = None, limit: int = None) -> list[dict]:
    """Load crash site coordinates from the seed CSV."""
    sites = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row.get("site_id", "").startswith("#") or not row.get("site_id", "").strip():
                continue
            if class_filter and row["class_label"] != class_filter:
                continue
            sites.append({
                "site_id": row["site_id"].strip(),
                "class_label": row["class_label"].strip(),
                "name": row["name"].strip(),
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
                "year": int(row["year"]),
                "source": row["source"].strip(),
                "notes": row.get("notes", "").strip(),
            })
            if limit and len(sites) >= limit:
                break
    return sites


def lat_lon_to_bbox(lat: float, lon: float, half_extent_m: float = HALF_EXTENT) -> list[float]:
    """
    Convert a lat/lon center point to a bounding box [west, south, east, north].
    Uses approximate meter-to-degree conversion.
    """
    lat_deg_per_m = 1 / 111320
    lon_deg_per_m = 1 / (111320 * np.cos(np.radians(lat)))

    west = lon - (half_extent_m * lon_deg_per_m)
    east = lon + (half_extent_m * lon_deg_per_m)
    south = lat - (half_extent_m * lat_deg_per_m)
    north = lat + (half_extent_m * lat_deg_per_m)

    return [west, south, east, north]


def search_sentinel2_scenes(bbox: list[float], year: int, max_cloud: int = 20) -> list[dict]:
    """
    Search Planetary Computer STAC API for Sentinel-2 L2A scenes
    covering the given bounding box, preferring dates near the crash year.
    """
    start_date = f"{max(year, 2017)}-01-01"  # Sentinel-2 L2A starts ~2017
    end_date = f"{min(year + 3, 2025)}-12-31"

    search_url = f"{STAC_API_URL}/search"
    payload = {
        "collections": ["sentinel-2-l2a"],
        "bbox": bbox,
        "datetime": f"{start_date}/{end_date}",
        "query": {
            "eo:cloud_cover": {"lt": max_cloud}
        },
        "sortby": [{"field": "properties.eo:cloud_cover", "direction": "asc"}],
        "limit": 5,
    }

    try:
        resp = requests.post(search_url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("features", [])
    except requests.RequestException as e:
        print(f"  [ERROR] STAC search failed: {e}")
        return []


def sign_planetary_computer_url(href: str) -> str:
    """Sign a Planetary Computer asset URL for access (free, no key needed)."""
    sign_url = "https://planetarycomputer.microsoft.com/api/sas/v1/sign"
    try:
        resp = requests.get(sign_url, params={"href": href}, timeout=15)
        resp.raise_for_status()
        return resp.json()["href"]
    except requests.RequestException:
        return href


def download_rgb_tile(scene: dict, bbox: list[float], output_path: str) -> bool:
    """
    Download and compose an RGB tile from a Sentinel-2 scene.
    Uses the rendered preview if available, otherwise composes from B04/B03/B02.
    """
    assets = scene.get("assets", {})

    # Try the pre-composed visual/TCI band first
    visual_key = None
    for key in ["visual", "rendered_preview", "preview"]:
        if key in assets:
            visual_key = key
            break

    if visual_key:
        href = assets[visual_key].get("href", "")
        signed_url = sign_planetary_computer_url(href)
        return _download_and_crop(signed_url, bbox, output_path)

    # Fall back to composing from individual bands
    band_keys = {"red": "B04", "green": "B03", "blue": "B02"}
    bands = {}
    for color, band_id in band_keys.items():
        for asset_key, asset_val in assets.items():
            if band_id.lower() in asset_key.lower():
                bands[color] = sign_planetary_computer_url(asset_val["href"])
                break

    if len(bands) == 3:
        return _download_bands_and_compose(bands, bbox, output_path)

    print(f"  [WARN] Could not find usable bands in scene")
    return False


def _download_and_crop(url: str, bbox: list[float], output_path: str) -> bool:
    """Download a visual tile, crop to bounding box, and save."""
    try:
        try:
            import rasterio
            from rasterio.windows import from_bounds

            with rasterio.open(url) as src:
                window = from_bounds(*bbox, transform=src.transform)
                data = src.read([1, 2, 3], window=window)
                img = np.transpose(data, (1, 2, 0))  # CHW -> HWC
                pil_img = Image.fromarray(img.astype(np.uint8))
                pil_img = pil_img.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
                pil_img.save(output_path)
                return True

        except ImportError:
            # Fallback without rasterio: download preview thumbnail
            resp = requests.get(url, timeout=60, stream=True)
            resp.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            img = Image.open(output_path)
            img = img.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
            img.save(output_path)
            return True

    except Exception as e:
        print(f"  [ERROR] Download failed: {e}")
        return False


def _download_bands_and_compose(band_urls: dict, bbox: list, output_path: str) -> bool:
    """Download individual R/G/B bands and compose into an RGB image."""
    try:
        import rasterio
        from rasterio.windows import from_bounds

        channels = []
        for color in ["red", "green", "blue"]:
            with rasterio.open(band_urls[color]) as src:
                window = from_bounds(*bbox, transform=src.transform)
                band_data = src.read(1, window=window)
                channels.append(band_data)

        rgb = np.stack(channels, axis=-1).astype(np.float32)
        rgb = np.clip(rgb / 3000 * 255, 0, 255).astype(np.uint8)

        pil_img = Image.fromarray(rgb)
        pil_img = pil_img.resize((TILE_SIZE, TILE_SIZE), Image.LANCZOS)
        pil_img.save(output_path)
        return True

    except Exception as e:
        print(f"  [ERROR] Band composition failed: {e}")
        return False


def download_site(site: dict, output_dir: str) -> dict:
    """
    Download a satellite tile for a single crash site.
    Returns metadata about the download.
    """
    site_id = site["site_id"]
    class_label = site["class_label"]
    lat, lon = site["latitude"], site["longitude"]
    year = site["year"]

    class_dir = os.path.join(output_dir, class_label)
    os.makedirs(class_dir, exist_ok=True)

    output_path = os.path.join(class_dir, f"{site_id}.png")

    if os.path.exists(output_path):
        print(f"  [SKIP] {site_id} already exists")
        return {"site_id": site_id, "status": "skipped", "path": output_path}

    print(f"  Searching for imagery near ({lat:.4f}, {lon:.4f}), year {year}...")

    bbox = lat_lon_to_bbox(lat, lon)
    scenes = search_sentinel2_scenes(bbox, year)

    if not scenes:
        scenes = search_sentinel2_scenes(bbox, year, max_cloud=50)

    if not scenes:
        print(f"  [WARN] No scenes found for {site_id}")
        return {"site_id": site_id, "status": "no_scenes", "path": None}

    best_scene = scenes[0]
    scene_date = best_scene.get("properties", {}).get("datetime", "unknown")
    cloud_cover = best_scene.get("properties", {}).get("eo:cloud_cover", "?")
    print(f"  Found scene: date={scene_date}, cloud={cloud_cover}%")

    success = download_rgb_tile(best_scene, bbox, output_path)

    if success:
        print(f"  [OK] Saved to {output_path}")
        return {
            "site_id": site_id,
            "status": "downloaded",
            "path": output_path,
            "scene_date": scene_date,
            "cloud_cover": cloud_cover,
        }
    else:
        print(f"  [FAIL] Could not download {site_id}")
        return {"site_id": site_id, "status": "failed", "path": None}


def main():
    parser = argparse.ArgumentParser(
        description="CrashSight AI — Download satellite imagery for known crash sites"
    )
    parser.add_argument("--csv", default="data/seed_sites.csv",
                        help="Path to seed sites CSV")
    parser.add_argument("--output", default="data/raw/",
                        help="Output directory for downloaded tiles")
    parser.add_argument("--class", dest="class_filter", default=None,
                        help="Download only this crash class (e.g., PLANE_FOREST)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max number of sites to download")
    parser.add_argument("--dry-run", action="store_true",
                        help="List sites without downloading")
    args = parser.parse_args()

    print("=" * 60)
    print("CrashSight AI — Satellite Imagery Downloader")
    print("=" * 60)

    sites = load_seed_sites(args.csv, class_filter=args.class_filter, limit=args.limit)
    print(f"\nLoaded {len(sites)} sites from {args.csv}")

    if args.class_filter:
        print(f"Filtered to class: {args.class_filter}")

    if args.dry_run:
        print("\n[DRY RUN] Sites that would be downloaded:")
        for s in sites:
            print(f"  {s['site_id']} | {s['class_label']} | {s['name']} | ({s['latitude']}, {s['longitude']})")
        return

    os.makedirs(args.output, exist_ok=True)

    results = {"downloaded": 0, "skipped": 0, "failed": 0, "no_scenes": 0}
    for i, site in enumerate(sites, 1):
        print(f"\n[{i}/{len(sites)}] {site['site_id']} — {site['name']}")
        result = download_site(site, args.output)
        results[result["status"]] = results.get(result["status"], 0) + 1

    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    for status, count in results.items():
        print(f"  {status}: {count}")
    print(f"\nTiles saved to: {args.output}")
    print("Next step: Inspect tiles and begin annotation (see docs/labelling_guides/)")


if __name__ == "__main__":
    main()
