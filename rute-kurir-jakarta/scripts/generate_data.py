"""Bangkitkan data/nodes.csv, data/edges.csv, data/scenarios.csv (deterministik)."""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from rute.data import LOCATIONS, build_edges, build_scenarios  # noqa: E402


def main() -> None:
    out = ROOT / "data"
    out.mkdir(exist_ok=True)
    with open(out / "nodes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "name", "lat", "lon", "role"])
        for i, name, lat, lon in LOCATIONS:
            w.writerow([i, name, lat, lon, "depot" if i == 0 else "stop"])
    edges = build_edges()
    with open(out / "edges.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["u", "v", "km"])
        w.writerows(edges)
    sc = build_scenarios()
    with open(out / "scenarios.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["scenario", "depot", "n_stops", "stops"])
        for name, stops in sc.items():
            w.writerow([name, 0, len(stops), ";".join(map(str, stops))])
    print(f"nodes={len(LOCATIONS)} edges={len(edges)} scenarios={len(sc)}")


if __name__ == "__main__":
    main()
