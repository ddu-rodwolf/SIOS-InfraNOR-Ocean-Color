## ⚠️ Disclaimer

This script is intended for **demonstration and exploratory purposes** only.  
It uses CHL-a as a biomass proxy with a constant Mixed Layer Depth (MLD). No validation is performed against in situ measurements.

Do **not** use this output for operational decision-making or scientific publication without proper review.

# Estimating Phytoplankton Biomass from OceanColor CHL-a (Svalbard Region)

This Python script visualizes and estimates phytoplankton biomass using **Chlorophyll-a (CHL-a)** data from the [SIOS InfraNOR OceanColor Arctic 1km product](https://thredds.nersc.no/thredds/catalog/sios_infranor_oceancolor/arctic_1km_oceancolor/catalog.html).

It is meant as a demonstration of using CHL-a as a **biomass proxy**, and includes steps for both:
- Plotting CHL-a concentrations on a specific date
- Computing a rough biomass estimate based on a user-defined Mixed Layer Depth (MLD)

## 🌊 Dataset

- Source: Copernicus Marine - OceanColor Arctic 1km
- Format: netCDF4 via OPeNDAP or downloaded `.nc` file
- Variable used: `CHL` (Chlorophyll-a concentration in mg/m³)

## 📊 What the script does
 === PART 1: Load dataset and prepare for plotting ===

1. Load NetCDF
2. Extract lat/lon/CHL/time
3. Handle _FillValue, NaN
4. Mask invalid values → CHL4P
5. Plot CHL4P with log scale
6. Add hatching for missing values
7. Add legend, title, axes

 === PART 2: Biomass estimation ===

1. Define compute_biomass_estimates()  
   Biomass (mg) = CHL-a (mg/m³) × MLD (m) × area (m²)
3. Reuse CHL4P to calculate total biomass
4. Print result to terminal
5. Add biomass text block under plot

## 📁 File

- `CHL-a-Svalbard_v02.00.py`: Main script

## 🔧 Requirements

- Python 3.x
- `numpy`, `matplotlib`, `netCDF4`

Install with:

```bash
pip install numpy matplotlib netCDF4
