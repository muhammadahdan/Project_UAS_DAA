"""Visualisasi rute (opsional, butuh matplotlib)."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_route(graph, route, out_path: str, title: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(8, 7))
    for u, nbrs in graph.adj.items():  # ruas jalan (abu-abu)
        for v, _ in nbrs:
            if u < v:
                (la1, lo1), (la2, lo2) = graph.coords[u], graph.coords[v]
                ax.plot([lo1, lo2], [la1, la2], color="#d0d0d0", lw=0.8, zorder=1)
    xs = [graph.coords[v][1] for v in route.road_path]
    ys = [graph.coords[v][0] for v in route.road_path]
    ax.plot(xs, ys, color="#c0392b", lw=2.2, zorder=2, label="Rute")
    visited = set(route.order[1:])
    for v, (la, lo) in graph.coords.items():
        if v == route.order[0]:
            ax.scatter(lo, la, s=120, marker="*", color="#1f3a93", zorder=4, label="Depo")
        elif v in visited:
            ax.scatter(lo, la, s=36, color="#e67e22", zorder=3)
            ax.annotate(str(route.order.index(v)), (lo, la), fontsize=7, xytext=(3, 3), textcoords="offset points")
        else:
            ax.scatter(lo, la, s=12, color="#999999", zorder=2)
    ax.set_title(title or f"{route.method}: {route.cost_km:.1f} km, {len(route.order) - 1} titik")
    ax.set_xlabel("Bujur")
    ax.set_ylabel("Lintang")
    ax.legend(loc="lower left")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
