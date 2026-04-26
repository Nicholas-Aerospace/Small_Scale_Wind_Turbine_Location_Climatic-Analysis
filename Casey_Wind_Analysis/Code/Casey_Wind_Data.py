import meteostat as ms 
import matplotlib.pyplot as plt
from datetime import date
import pandas as pd
import numpy as np
#Preamble to make the code buzz
ms.config.block_large_requests = False
#Allows fetching of data beyond 3 years without being blocked by the server
station_ID = 89611 
#WMO identifier for Casey Station
start = date(2019, 1, 1)
end = date(2025, 12, 31)
#Time period for data collection

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

# Set 1: Single representative year (day of year 1–366)
df_avg_year = df.groupby(df.index.day_of_year).mean()

# Set 2: Average day for each month (month 1–12, hour 0–23)
df_avg_day_by_month = df.groupby([df.index.month, df.index.hour]).mean()


avg_wspd = df['wspd'].mean()
avg_wdir = df['wdir'].mean()
avg_temp = df['temp'].mean()
avg_prcp = df['prcp'].mean()
avg_pres = df['pres'].mean()


# ── Betz Power Function ───────────────────────────────────────────────────────
# P = (8/27) * rho * A * v^3
# rho = P / (Rd * T)  — dry air density
# A = pi * r^2 = pi * 2^2 = 12.57 m^2
# Note: wspd from meteostat is in km/h — must convert to m/s

Rd = 287.05       # J/(kg·K)
A  = np.pi * 2**2 # m^2 — blade radius of 2m

def betz_power(wspd_kmh, pres_hpa, temp_c):
    """Returns Betz limit power in Watts"""
    v   = wspd_kmh / 3.6                           # km/h → m/s
    T   = temp_c + 273.15                           # °C → K
    P   = pres_hpa * 100                            # hPa → Pa
    rho = P / (Rd * T)                              # kg/m³
    return (8/27) * rho * A * v**3                  # Watts

# ── Power over the averaged year (one value per day of year) ──────────────────
df_avg_year['power'] = betz_power(
    df_avg_year['wspd'],
    df_avg_year['pres'],
    df_avg_year['temp']
)

# ── Power over the averaged day for each month ────────────────────────────────
df_avg_day_by_month['power'] = betz_power(
    df_avg_day_by_month['wspd'],
    df_avg_day_by_month['pres'],
    df_avg_day_by_month['temp']
)

# ── Grand average power ───────────────────────────────────────────────────────
avg_power = betz_power(avg_wspd, avg_pres, avg_temp)

# ── Plotting ──────────────────────────────────────────────────────────────────
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
colors = plt.cm.tab20(range(12))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle("Casey Station (89611) — Betz Limit Wind Power (r = 2m)", fontsize=14, fontweight='bold')

# --- Plot 1: Power across the averaged year ---
ax1 = axes[0]
ax1.plot(df_avg_year.index, df_avg_year['power'], color='steelblue', linewidth=1.5)
ax1.axhline(avg_power, color='red', linestyle='--', linewidth=1.2,
            label=f'Annual Mean: {avg_power:.1f} W')
ax1.set_title("Max Available Power by Day of Year (2019–2025)")
ax1.set_xlabel("Day of Year")
ax1.set_ylabel("Power (W)")
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# --- Plot 2: Power across the averaged day for each month ---
ax2 = axes[1]
for month in range(1, 13):
    profile = df_avg_day_by_month.loc[month]['power']
    ax2.plot(profile.index, profile.values,
             label=month_names[month - 1], color=colors[month - 1], linewidth=1.5)
ax2.axhline(avg_power, color='black', linestyle='--', linewidth=2,
            label=f'Overall Mean: {avg_power:.1f} W')
ax2.set_title("Max Available Power by Hour of Day per Month")
ax2.set_xlabel("Hour of Day")
ax2.set_ylabel("Power (W)")
ax2.set_xticks(range(0, 24))
ax2.legend(loc='upper right', ncol=4, fontsize=8)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
