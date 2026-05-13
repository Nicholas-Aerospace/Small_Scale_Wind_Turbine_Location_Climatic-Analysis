# Casey Station and Kunayni Wind Analysis

A basic wind analysis of Casey station (WMO:89611) in Antarctica to determine the estimated maximum power output of a small scale wind turbine. The code uses weather data over 2019-2025.

Another wind analysis was undertaken for various sizes of Vertical Axis Wind Turbines (VAWT) and Horizontal Axis Wind Turbines (HAWT) on Kunayni/Mt Wellington using the ideal betz limit to estimate the maximum possible power generation from this location
## Introduction

The purpose of the code was to determine the maximum possible power available using the Betz limit, the approach is very rough but was produced for the purpose of informing a design brief so accuracy was not required. The small turbine used in the simulation has a radius of 2m and is 5m above the ground for Casey station and various sizes for Kunayni.

---
## AI Use Statement:
The AI Claude was used to produce comments and troubleshoot the code and alos producing sections of the code.

## Dependencies

### Required Software
- Python 3.9+

### Python Dependencies
meteostat: https://dev.meteostat.net/python

matplotLib:https://matplotlib.org/

## Results

### Some of the Available Wind Averages
<img width="2633" height="1036" alt="hawt_radius_vs_power" src="https://github.com/user-attachments/assets/f43308b4-95bf-4771-9492-f4c648cb2a16" />
<img width="3014" height="1967" alt="vawt_monthly_heatmap" src="https://github.com/user-attachments/assets/0328ab56-ecde-4997-8c3e-64dd23a9e1d1" />
<img width="3614" height="2267" alt="vawt_hourly_heatmap" src="https://github.com/user-attachments/assets/266aaefc-15be-442a-8b1a-db0e66ab8d3d" />
<img width="1504" height="894" alt="Kunayni Wind Analysis" src="https://github.com/user-attachments/assets/a4a1f152-38e3-4d9b-82ea-0c9cae39d33e" />
<img width="1506" height="500" alt="Kunayni Climate Analysis" src="https://github.com/user-attachments/assets/be0d84da-f8e5-4e6f-b24b-156032fd4205" />

