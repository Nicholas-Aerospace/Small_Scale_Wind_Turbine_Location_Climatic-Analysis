import meteostat as ms
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D
from datetime import date
import pandas as pd
import numpy as np

# ── Blade Radius Sweep Configuration ─────────────────────────────────────────
min_radius = 0.5    # metres
max_radius = 5.0    # metres
n_steps    = 200    # resolution of the radius axis

radii = np.linspace(min_radius, max_radius, n_steps)

# ── Meteostat Setup ───────────────────────────────────────────────────────────
ms.config.block_large_requests = False

station_ID = 95979   # Kunayni

start = date(2019, 1, 1)
end   = date(2025, 12, 31)

ts = ms.hourly(
    ms.Station(id=station_ID),
    start,
    end,
    parameters=[
        ms.Parameter.TEMP,
        ms.Parameter.PRCP,
        ms.Parameter.WSPD,
        ms.Parameter.WPGT,
        ms.Parameter.WDIR,
        ms.Parameter.PRES
    ]
)

df = ts.fetch()

# ── Averaging ─────────────────────────────────────────────────────────────────
# Monthly averages  →  12 rows  (one per calendar month)
df_monthly = df.groupby(df.index.month)[['wspd', 'pres', 'temp']].mean()

# Hourly averages   →  24 rows  (one per hour of the day, across all years)
df_hourly  = df.groupby(df.index.hour)[['wspd', 'pres', 'temp']].mean()

# Grand average
avg_wspd = df['wspd'].mean()
avg_temp = df['temp'].mean()
avg_pres = df['pres'].mean()

# ── Betz Power Function ───────────────────────────────────────────────────────
Rd = 287.05  # J/(kg·K)

def betz_power(wspd_kmh, pres_hpa, temp_c, blade_radius):
    v   = wspd_kmh / 3.6
    T   = temp_c  + 273.15
    P   = pres_hpa * 100
    rho = P / (Rd * T)
    A   = np.pi * blade_radius**2
    return (8/27) * rho * A * v**3

# ── Precompute power curves ───────────────────────────────────────────────────
power_by_month = np.array([
    betz_power(row.wspd, row.pres, row.temp, radii)
    for _, row in df_monthly.iterrows()
])

power_by_hour = np.array([
    betz_power(row.wspd, row.pres, row.temp, radii)
    for _, row in df_hourly.iterrows()
])

power_grand = betz_power(avg_wspd, avg_pres, avg_temp, radii)

# ── Plot Labels & Colour Maps ─────────────────────────────────────────────────
month_names  = ['Jan','Feb','Mar','Apr','May','Jun',
                'Jul','Aug','Sep','Oct','Nov','Dec']
month_colors = cm.tab20(np.linspace(0, 1, 12))
hour_colors  = cm.plasma(np.linspace(0.05, 0.95, 24))

# ── Figure ────────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle(
    "Kunayni (95979) — Betz Limit Power vs Blade Radius",
    fontsize=15, fontweight='bold'
)

# ── Plot 1: One curve per MONTH ───────────────────────────────────────────────
for i, name in enumerate(month_names):
    ax1.plot(radii, power_by_month[i],
             color=month_colors[i], linewidth=1.8, label=name)

ax1.plot(radii, power_grand,
         color='black', linewidth=2.5, linestyle='--',
         label='Annual Mean', zorder=5)

ax1.set_title("Calendar Month", fontsize=11)
ax1.set_xlabel("Blade Radius (m)", fontsize=11)
ax1.set_ylabel("Betz Limit Power (W)", fontsize=11)
ax1.legend(ncol=2, fontsize=8, loc='upper left', framealpha=0.85)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(min_radius, max_radius)
ax1.set_ylim(bottom=0)

# Secondary x-axis: diameter
ax1b = ax1.twiny()
ax1b.set_xlim(min_radius * 2, max_radius * 2)
ax1b.set_xlabel("Rotor Diameter (m)", fontsize=10, color='grey')
ax1b.tick_params(axis='x', colors='grey')

# ── Plot 2: One curve per HOUR of day ────────────────────────────────────────
for h in range(24):
    ax2.plot(radii, power_by_hour[h],
             color=hour_colors[h], linewidth=1.4)

ax2.plot(radii, power_grand,
         color='black', linewidth=2.5, linestyle='--',
         label='Overall Mean', zorder=5)

ax2.set_title("By Hour of Day (UTC)", fontsize=11)
ax2.set_xlabel("Blade Radius (m)", fontsize=11)
ax2.set_ylabel("Betz Limit Power (W)", fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(min_radius, max_radius)
ax2.set_ylim(bottom=0)

# Colour-bar for hours
sm = cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=0, vmax=23))
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax2, pad=0.02, aspect=30)
cbar.set_label("Hour of Day (UTC)", fontsize=10)
cbar.set_ticks([0, 6, 12, 18, 23])
cbar.set_ticklabels(['00:00', '06:00', '12:00', '18:00', '23:00'])

ax2.legend(handles=[
    Line2D([0], [0], color='black', linewidth=2.5,
           linestyle='--', label='Overall Mean')
], fontsize=9, loc='upper left')

plt.tight_layout()
plt.savefig("hawt_radius_vs_power.png", dpi=150, bbox_inches='tight')
plt.show()
print("Done — plot saved as hawt_radius_vs_power.png")