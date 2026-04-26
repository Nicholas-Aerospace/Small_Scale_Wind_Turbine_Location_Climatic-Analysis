import matplotlib.pyplot as plt
from Kunayni_Wind_Data_HAWT import df_avg_year, df_avg_day_by_month, avg_wspd, avg_wdir, avg_temp, avg_prcp, avg_pres

# ── Plotting ──────────────────────────────────────────────────────────────────
month_names = ['Jan','Feb','Mar','Apr','May','Jun',
               'Jul','Aug','Sep','Oct','Nov','Dec']
colors = plt.cm.tab20(range(12))

# ── Figure 1: Wind ────────────────────────────────────────────────────────────
fig1, axes = plt.subplots(2, 2, figsize=(16, 10))
fig1.suptitle("Kunayni (95979) — Wind Analysis", fontsize=14, fontweight='bold')

# --- Plot 1: Wind Speed across the year ---
ax1 = axes[0, 0]
ax1.plot(df_avg_year.index, df_avg_year['wspd'], color='steelblue', linewidth=1.5)
ax1.axhline(avg_wspd, color='red', linestyle='--', linewidth=1.2, label=f'Annual Mean: {avg_wspd:.1f} km/h')
ax1.set_title("Average Wind Speed by Day of Year (2019–2025)")
ax1.set_xlabel("Day of Year")
ax1.set_ylabel("Wind Speed (km/h)")
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3)

# --- Plot 2: Wind Direction across the year ---
ax2 = axes[0, 1]
ax2.plot(df_avg_year.index, df_avg_year['wdir'], color='darkorange', linewidth=1.5)
ax2.axhline(avg_wdir, color='red', linestyle='--', linewidth=1.2, label=f'Annual Mean: {avg_wdir:.1f}°')
ax2.set_title("Average Wind Direction by Day of Year (2019–2025)")
ax2.set_xlabel("Day of Year")
ax2.set_ylabel("Wind Direction (°)")
ax2.set_yticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
ax2.set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

# --- Plot 3: Hourly Wind Speed profile per month ---
ax3 = axes[1, 0]
for month in range(1, 13):
    profile = df_avg_day_by_month.loc[month]['wspd']
    ax3.plot(profile.index, profile.values,
             label=month_names[month - 1], color=colors[month - 1], linewidth=1.5)
ax3.axhline(avg_wspd, color='black', linestyle='--', linewidth=2, label=f'Daily Mean: {avg_wspd:.1f} km/h')
ax3.set_title("Average Hourly Wind Speed per Month")
ax3.set_xlabel("Hour of Day")
ax3.set_ylabel("Wind Speed (km/h)")
ax3.set_xticks(range(0, 24))
ax3.legend(loc='lower right', ncol=4, fontsize=8)
ax3.grid(True, alpha=0.3)

# --- Plot 4: Hourly Wind Direction profile per month ---
ax4 = axes[1, 1]
for month in range(1, 13):
    profile = df_avg_day_by_month.loc[month]['wdir']
    ax4.plot(profile.index, profile.values,
             label=month_names[month - 1], color=colors[month - 1], linewidth=1.5)
ax4.axhline(avg_wdir, color='black', linestyle='--', linewidth=2, label=f'Daily Mean: {avg_wdir:.1f}°')
ax4.set_title("Average Hourly Wind Direction per Month")
ax4.set_xlabel("Hour of Day")
ax4.set_ylabel("Wind Direction (°)")
ax4.set_xticks(range(0, 24))
ax4.set_yticks([0, 45, 90, 135, 180, 225, 270, 315, 360])
ax4.set_yticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N'])
ax4.legend(loc='upper right', ncol=4, fontsize=8)
ax4.grid(True, alpha=0.3)

fig1.tight_layout()

# ── Figure 2: Climate ─────────────────────────────────────────────────────────
fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))
fig2.suptitle("Kunayni (95979) — Climate Analysis", fontsize=14, fontweight='bold')

# --- Plot 5: Temperature ---
ax5 = axes2[0]
ax5.plot(df_avg_year.index, df_avg_year['temp'], color='tomato', linewidth=1.5)
ax5.axhline(avg_temp, color='black', linestyle='--', linewidth=1.2, label=f'Annual Mean: {avg_temp:.1f}°C')
ax5.axhline(0, color='grey', linestyle=':', linewidth=1, label='0°C')
ax5.set_title("Average Temperature by Day of Year (2019–2025)")
ax5.set_xlabel("Day of Year")
ax5.set_ylabel("Temperature (°C)")
ax5.legend(fontsize=9)
ax5.grid(True, alpha=0.3)

# --- Plot 6: Precipitation ---
ax6 = axes2[1]
ax6.bar(df_avg_year.index, df_avg_year['prcp'], color='cornflowerblue', width=1.0)
ax6.axhline(avg_prcp, color='black', linestyle='--', linewidth=1.2, label=f'Annual Mean: {avg_prcp:.2f} mm')
ax6.set_title("Average Precipitation by Day of Year (2019–2025)")
ax6.set_xlabel("Day of Year")
ax6.set_ylabel("Precipitation (mm)")
ax6.legend(fontsize=9)
ax6.grid(True, alpha=0.3)

# --- Plot 7: Pressure ---
ax7 = axes2[2]
ax7.plot(df_avg_year.index, df_avg_year['pres'], color='mediumpurple', linewidth=1.5)
ax7.axhline(avg_pres, color='black', linestyle='--', linewidth=1.2, label=f'Annual Mean: {avg_pres:.1f} hPa')
ax7.set_title("Average Pressure by Day of Year (2019–2025)")
ax7.set_xlabel("Day of Year")
ax7.set_ylabel("Pressure (hPa)")
ax7.legend(fontsize=9)
ax7.grid(True, alpha=0.3)

fig2.tight_layout()
plt.show()