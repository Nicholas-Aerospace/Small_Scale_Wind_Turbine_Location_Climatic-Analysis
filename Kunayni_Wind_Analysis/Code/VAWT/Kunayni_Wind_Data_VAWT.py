import meteostat as ms
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from datetime import date
import numpy as np

# ── Sweep Configuration ───────────────────────────────────────────────────────
min_radius  = 0.5    # metres
max_radius  = 3.0    # metres
min_hr      = 0.5    # H/R ratio (height = ratio × radius)
max_hr      = 5.0    # H/R ratio
n_grid      = 80     # grid resolution (n × n heatmap cells)

Cp = 0.593           # Betz limit
Rd = 287.05          # J/(kg·K)

radii  = np.linspace(min_radius, max_radius, n_grid)
hr_ratios = np.linspace(min_hr, max_hr, n_grid)
R, HR = np.meshgrid(radii, hr_ratios)   # shape (n_grid, n_grid)

# ── Meteostat Setup ───────────────────────────────────────────────────────────
ms.config.block_large_requests = False

station_ID = 95979
start = date(2019, 1, 1)
end   = date(2025, 12, 31)

ts = ms.hourly(
    ms.Station(id=station_ID), start, end,
    parameters=[
        ms.Parameter.TEMP, ms.Parameter.PRCP, ms.Parameter.WSPD,
        ms.Parameter.WPGT, ms.Parameter.WDIR, ms.Parameter.PRES
    ]
)
df = ts.fetch()

# ── Averaging ─────────────────────────────────────────────────────────────────
df_monthly = df.groupby(df.index.month)[['wspd', 'pres', 'temp']].mean()
df_hourly  = df.groupby(df.index.hour)[['wspd', 'pres', 'temp']].mean()

# ── VAWT Power Function (broadcast over 2-D grid) ────────────────────────────
def vawt_power_grid(wspd_kmh, pres_hpa, temp_c, R_grid, HR_grid):
    """
    R_grid  : 2-D array of blade radii (m)
    HR_grid : 2-D array of H/R ratios
    Returns power grid in Watts.
    """
    v   = wspd_kmh / 3.6
    T   = temp_c  + 273.15
    P   = pres_hpa * 100
    rho = P / (Rd * T)
    H   = HR_grid * R_grid           # height = ratio × radius
    A   = 2 * R_grid * H             # frontal area = 2r × H
    return Cp * 0.5 * rho * A * v**3

# ── Precompute all power grids ────────────────────────────────────────────────
monthly_grids = [
    vawt_power_grid(row.wspd, row.pres, row.temp, R, HR)
    for _, row in df_monthly.iterrows()
]  # list of 12 arrays, each (n_grid, n_grid)

hourly_grids = [
    vawt_power_grid(row.wspd, row.pres, row.temp, R, HR)
    for _, row in df_hourly.iterrows()
]  # list of 24 arrays

# Shared colour scale across both figures
all_power = np.concatenate([g.ravel() for g in monthly_grids + hourly_grids])
vmin, vmax = 0, np.percentile(all_power, 98)   # clip top 2% to avoid outliers dominating

month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']

# ────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — Monthly heatmaps  (3 rows × 4 cols)
# ────────────────────────────────────────────────────────────────────────────
fig1, axes1 = plt.subplots(3, 4, figsize=(20, 13), constrained_layout=True)
fig1.suptitle(
    "Kunayni (95979) — VAWT Power (W)  ·  Radius vs H/R Ratio  ·  By Month",
    fontsize=15, fontweight='bold'
)

norm = Normalize(vmin=vmin, vmax=vmax)
cmap = 'inferno'

for i, ax in enumerate(axes1.flat):
    pcm = ax.pcolormesh(radii, hr_ratios, monthly_grids[i],
                        cmap=cmap, norm=norm, shading='gouraud')
    # Overlay contour lines for readability
    cs = ax.contour(R, HR, monthly_grids[i],
                    levels=6, colors='white', linewidths=0.5, alpha=0.4)
    ax.clabel(cs, fmt='%d W', fontsize=6, colors='white')

    ax.set_title(month_names[i], fontsize=11, fontweight='bold')
    ax.set_xlabel("Radius (m)", fontsize=8)
    ax.set_ylabel("H/R Ratio", fontsize=8)
    ax.tick_params(labelsize=7)

# Shared colourbar
cbar1 = fig1.colorbar(
    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
    ax=axes1, fraction=0.02, pad=0.02
)
cbar1.set_label("Betz Power (W)", fontsize=11)

plt.savefig("vawt_monthly_heatmap.png", dpi=150, bbox_inches='tight')
plt.show()
print("Figure 1 saved → vawt_monthly_heatmap.png")

# ────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — Hourly heatmaps  (4 rows × 6 cols)
# ────────────────────────────────────────────────────────────────────────────
fig2, axes2 = plt.subplots(4, 6, figsize=(24, 15), constrained_layout=True)
fig2.suptitle(
    "Kunayni (95979) — VAWT Power (W)  ·  Radius vs H/R Ratio  ·  Average Day by Hour (UTC)",
    fontsize=15, fontweight='bold'
)

for h, ax in enumerate(axes2.flat):
    pcm = ax.pcolormesh(radii, hr_ratios, hourly_grids[h],
                        cmap=cmap, norm=norm, shading='gouraud')
    cs = ax.contour(R, HR, hourly_grids[h],
                    levels=5, colors='white', linewidths=0.4, alpha=0.35)
    ax.clabel(cs, fmt='%d W', fontsize=5, colors='white')

    ax.set_title(f"{h:02d}:00", fontsize=10, fontweight='bold')
    ax.set_xlabel("r (m)", fontsize=7)
    ax.set_ylabel("H/R", fontsize=7)
    ax.tick_params(labelsize=6)

cbar2 = fig2.colorbar(
    plt.cm.ScalarMappable(norm=norm, cmap=cmap),
    ax=axes2, fraction=0.015, pad=0.02
)
cbar2.set_label("Betz Power (W)", fontsize=11)

plt.savefig("vawt_hourly_heatmap.png", dpi=150, bbox_inches='tight')
plt.show()
print("Figure 2 saved → vawt_hourly_heatmap.png")

print("\nAll done.")