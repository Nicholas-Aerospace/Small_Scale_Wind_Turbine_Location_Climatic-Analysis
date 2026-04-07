# Casey Station Wind Analysis

A basic wind analysis of Casey station (WMO:89611) in Antarctica to determine the estimated maximum power output of a small scale wind turbine. The code uses weather data over 2019-2025.
## Introduction

The purpose of the code was to determine the maximum possible power available using the Betz limit, the approach is very rough but was produced for the purpose of informing a design brief so accuracy was not required. The small turbine used in the simulation has a radius of 2m and is 5m above the ground.

This code could easily be modified to determine max possible power outputs by changing the WMO station modifier to a different location in Casey_Wind_Data.py.

---
## AI Use Statement:
The AI Claude was used to produce comments and troubleshoot the code.

## Dependencies

### Required Software
- Python 3.9+

### Python Dependencies
meteostat: https://dev.meteostat.net/python

matplotLib:https://matplotlib.org/

## Results

### Wind Averages
<img width="1920" height="967" alt="Wind Analysis Plots" src="https://github.com/user-attachments/assets/762866a0-72e6-4cd3-907d-e0c69fc9e8a4" />
<img width="1800" height="500" alt="Climate Analysis" src="https://github.com/user-attachments/assets/c58aa9f2-580e-403e-a455-d4195d32c9c8" />

### Maxium Possible Power for a Horizontal Wind Turbine of 2m Radius
<img width="1600" height="600" alt="Power Figures" src="https://github.com/user-attachments/assets/4486e51b-f8ac-40a1-9c00-655756a61649" />
