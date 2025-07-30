# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 15:42:24 2023 (1st version)
Last version on Wed Jul 20 08:58:12 2023

@author: RudolfDenkmann
"""

###############################################################################################################

import os, sys
import netCDF4
import numpy as np
import matplotlib.pylab as plt
import matplotlib.colors as colors
from matplotlib.patches import Patch

# === PART 1: Load dataset and prepare for plotting ===

filename = "https://thredds.nersc.no/thredds/dodsC/sios_infranor_oceancolor/arctic_1km_oceancolor/2022/08/20220831_cmems_arctic1km_cmems_oceancolour.nc"
#filename = os.path.expanduser("~/Downloads/20220831_cmems_arctic1km_cmems_oceancolour.nc")
nc_ds    = netCDF4.Dataset(filename, "r")

lat  = nc_ds.variables["latitude"][:]
lon  = nc_ds.variables["longitude"][:]
time = nc_ds.variables["time"][:]
timestep = 0
mld = 20  # mixed layer depth in meters

# Load CHL and handle fill values
CHL_var  = nc_ds.variables["CHL"]
CHL4P    = np.array(CHL_var[timestep, :, :])  # Force load
fill_val = getattr(CHL_var, "_FillValue", -999.0)
CHL4P    = np.ma.masked_where((CHL4P == fill_val) | np.isnan(CHL4P), CHL4P)

# Plot chlorophyll-a
z_min = CHL4P[CHL4P > 0].min()
z_max = CHL4P.max()

fig, ax = plt.subplots(figsize=(7, 6))
c = plt.pcolormesh(lon, lat, CHL4P, norm=colors.LogNorm(vmin=z_min, vmax=z_max), cmap='summer_r')
cbar = plt.colorbar(c, label='mg/m³', spacing='uniform', format="{x:.1f}")

# Hatching for missing data
missing_mask = CHL4P.mask if np.ma.is_masked(CHL4P) else np.isnan(CHL4P)
ax.contourf(lon, lat, missing_mask, levels=[0.5, 1.5], hatches=['///'], colors='none', alpha=0)

# Legend for missing data
legend_elements = [Patch(facecolor='white', edgecolor='black', hatch='///', label='Missing data')]
ax.legend(handles=legend_elements, loc='lower right')

# Titles and labels
ax.set_xlabel('degree East')
ax.set_ylabel('degree North')
fig.suptitle('Chlorophyll-a concentration in sea water\n- Copernicus Marine - SIOS OceanColor -\n', 
             fontsize=12, fontweight='bold', y=0.95)

#plt.show()
#sys.exit()

# === PART 2: Compute and display biomass ===

def compute_biomass_estimates(CHL_array, mld, area_per_pixel_km2=1):
    """
    Estimate phytoplankton biomass from CHL-a using a constant mixed layer depth.
    
    Parameters:
    - CHL_array: 2D numpy array with CHL-a in mg/m³
    - mld: mixed layer depth in meters (default 20m)
    - area_per_pixel_km2: area per grid cell (default 1 km²)
    
    Returns:
    - biomass_kg, low_est_kg, high_est_kg: float values
    - text_block: tuple of strings to display or print
    """
    CHL_array = np.ma.filled(CHL_array, fill_value=0)  # Replace masked with 0
    CHL_array = np.where(CHL_array < 0, 0, CHL_array)  # Clip remaining negatives
    
    pixel_area_m2 = area_per_pixel_km2 * 1e6
    biomass_mg = np.sum(CHL_array) * mld * pixel_area_m2
    biomass_kg = biomass_mg / 1e6

    low_est_kg  = biomass_kg * 0.75  # MLD -25%
    high_est_kg = biomass_kg * 1.25  # MLD +25%

    text_block = (
        f"Total biomass: {biomass_kg:,.2f} kg\n"
        f"Low estimate (MLD -25%): {low_est_kg:,.2f} kg\n"
        f"High estimate (MLD +25%): {high_est_kg:,.2f} kg"
    )
    return biomass_kg, low_est_kg, high_est_kg, text_block

# Run biomass estimation
_, _, _, text_block = compute_biomass_estimates(CHL4P, mld)
print('\n' + text_block)

# Add biomass summary under plot
fig.text(0.5, -0.02, f"Estimated phytoplankton biomass from CHL-a (MLD = {mld} m)",
         ha='center', va='bottom', fontsize=10, fontweight='bold')
fig.text(0.5, -0.12, text_block, ha='center', va='bottom', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.85))

plt.tight_layout()
plt.show()
