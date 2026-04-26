import meteostat as ms 
import matplotlib.pyplot as plt
from datetime import date
import pandas as pd
import numpy as np
from itertools import product

# ── Sweep Configuration ───────────────────────────────────────────────────────
min_radius  = 1   # metres
max_radius  = 2   # metres
interval_r  = 0.5   # metres

min_height  = 1.0   # metres
max_height  = 4.0   # metres
interval_h  = 2.0   # metres

#Pure Betz limit Cp: 0.593
Cp = 0.593

radii   = np.arange(min_radius, max_radius + interval_r * 0.5, interval_r)
heights = np.arange(min_height, max_height + interval_h * 0.5, interval_h)
combos  = list(product(radii, heights))

# ── Meteostat Setup ───────────────────────────────────────────────────────────
ms.config.block_large_requests = False
# Allows fetching of data beyond 3 years without being blocked by the server

station_ID = 95979
# WMO identifier for Kunayni

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

# ── Averaging (computed once — independent of radius/height) ──────────────────
df_avg_year         = df.groupby(df.index.day_of_year).mean()
df_avg_day_by_month = df.groupby([df.index.month, df.index.hour]).mean()

avg_wspd = df['wspd'].mean()
avg_wdir = df['wdir'].mean()
avg_temp = df['temp'].mean()
avg_prcp = df['prcp'].mean()
avg_pres = df['pres'].mean()

# ── VAWT Power Function ───────────────────────────────────────────────────────
# P = Cp * 0.5 * rho * A * v³
# A = 2r * H   (full frontal rectangle — retreating blade penalty is in Cp)
# rho = P_atm / (Rd * T)
# wspd from meteostat is in km/h — must convert to m/s

Rd = 287.05  # J/(kg·K)

def vawt_power(wspd_kmh, pres_hpa, temp_c, blade_radius, turbine_height):
    """Returns VAWT power in Watts using real-world Cp."""
    v   = wspd_kmh / 3.6                    # km/h → m/s
    T   = temp_c + 273.15                   # °C → K
    P   = pres_hpa * 100                    # hPa → Pa
    rho = P / (Rd * T)                      # kg/m³
    A   = 2 * blade_radius * turbine_height # m² — full frontal rectangle
    return Cp * 0.5 * rho * A * v**3       # Watts

# ── Month Labels & Colours ────────────────────────────────────────────────────
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
colors = plt.cm.tab20(range(12))

# ── Run Simulation for Each (Radius, Height) Combination ─────────────────────
print(f"\nRunning {len(combos)} VAWT simulations "
      f"({len(radii)} radii × {len(heights)} heights)...\n")

for r, h in combos:
    print(f"  ── Blade radius: {r:.2f} m  |  Height: {h:.2f} m  "
          f"(⌀ {r*2:.2f} m  ·  A = {2*r*h:.2f} m²) ──")

    # --- Compute power columns for this radius/height ---
    df_avg_year_r         = df_avg_year.copy()
    df_avg_day_by_month_r = df_avg_day_by_month.copy()

    df_avg_year_r['power'] = vawt_power(
        df_avg_year_r['wspd'],
        df_avg_year_r['pres'],
        df_avg_year_r['temp'],
        r, h
    )

    df_avg_day_by_month_r['power'] = vawt_power(
        df_avg_day_by_month_r['wspd'],
        df_avg_day_by_month_r['pres'],
        df_avg_day_by_month_r['temp'],
        r, h
    )

    avg_power = vawt_power(avg_wspd, avg_pres, avg_temp, r, h)
    print(f"     Grand-average power: {avg_power:.2f} W")

    # --- Plotting ---
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle(
        f"Kunayni (95979) — VAWT Power  "
        f"r = {r:.2f} m  ·  H = {h:.2f} m  (⌀ {r*2:.2f} m  ·  A = {2*r*h:.2f} m²)",
        fontsize=14, fontweight='bold'
    )

    # Plot 1: Power across the averaged year
    ax1 = axes[0]
    ax1.plot(df_avg_year_r.index, df_avg_year_r['power'], color='steelblue', linewidth=1.5)
    ax1.axhline(avg_power, color='red', linestyle='--', linewidth=1.2,
                label=f'Annual Mean: {avg_power:.1f} W')
    ax1.set_title("Max Available Power by Day of Year (2019–2025)")
    ax1.set_xlabel("Day of Year")
    ax1.set_ylabel("Power (W)")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Plot 2: Power across the averaged day for each month
    ax2 = axes[1]
    for month in range(1, 13):
        profile = df_avg_day_by_month_r.loc[month]['power']
        ax2.plot(profile.index, profile.values,
                 label=month_names[month - 1], color=colors[month - 1], linewidth=1.5)
    ax2.axhline(avg_power, color='black', linestyle='--', linewidth=2,
                label=f'Overall Mean: {avg_power:.1f} W')
    ax2.set_title("Max Available Power by Hour of Day per Month")
    ax2.set_xlabel("Hour of Day UTC")
    ax2.set_ylabel("Power (W)")
    ax2.set_xticks(range(0, 24))
    ax2.legend(loc='upper right', ncol=4, fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

print("\nAll simulations complete.")