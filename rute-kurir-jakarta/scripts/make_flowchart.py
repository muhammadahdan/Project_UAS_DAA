"""Gambar diagram alur solusi (D03) ke outputs/figures/diagram_alur.png."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "outputs" / "figures" / "diagram_alur.png"

fig, ax = plt.subplots(figsize=(8, 9.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis("off")


def box(x, y, w, h, text, color="#e8f0fe", shape="round"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=f"{shape},pad=0.05",
                                fc=color, ec="#33415c", lw=1.2))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5)


def arrow(x1, y1, x2, y2, label=""):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color="#33415c"))
    if label:
        ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2, label, fontsize=8, color="#b03a2e")


box(5, 11.3, 5.2, 0.8, "Mulai: graf jalan + depo + daftar titik antar", "#d5f5e3")
box(5, 10.0, 5.2, 0.8, "Validasi: buang duplikat/depo, cek id dikenal", "#fdebd0")
arrow(5, 10.9, 5, 10.4)
box(5, 8.7, 5.6, 0.8, "Dijkstra dari tiap titik -> matriks jarak terpendek d", "#e8f0fe")
arrow(5, 9.6, 5, 9.1)
box(5, 7.4, 5.6, 0.8, "Semua titik terjangkau dari depo?", "#fdebd0", "square")
arrow(5, 8.3, 5, 7.8)
box(9.0, 7.4, 1.8, 0.8, "Galat\nValueError", "#f5b7b1")
arrow(7.8, 7.4, 8.1, 7.4, "tidak")
box(5, 6.1, 4.4, 0.8, "Jumlah titik k <= 15 ?", "#fdebd0", "square")
arrow(5, 7.0, 5, 6.5, "ya")
box(2.3, 4.6, 3.6, 1.0, "Held-Karp (DP bitmask)\nrute OPTIMAL", "#d6eaf8")
box(7.7, 4.6, 3.6, 1.0, "Nearest Neighbor\n+ 2-opt\nrute heuristik", "#d6eaf8")
arrow(3.9, 5.8, 2.6, 5.1, "ya")
arrow(6.1, 5.8, 7.4, 5.1, "tidak")
box(5, 3.0, 5.6, 0.8, "Susun jalur jalan lengkap (prev Dijkstra) + total km", "#e8f0fe")
arrow(2.3, 4.1, 4.0, 3.4)
arrow(7.7, 4.1, 6.0, 3.4)
box(5, 1.7, 5.2, 0.8, "Keluaran: urutan kunjungan, jalur, total jarak", "#d5f5e3")
arrow(5, 2.6, 5, 2.1)
plt.tight_layout()
fig.savefig(OUT, dpi=170)
print("ok", OUT)
