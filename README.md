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

1. Loads CHL-a data from a specific date
2. Visualizes spatial CHL-a concentration on a map
3. Masks invalid/missing values and hatches them on the plot
4. Computes total phytoplankton biomass in kilograms using:
   \[
   \text{Biomass (mg)} = \text{CHL-a (mg/m³)} \times \text{MLD (m)} \times \text{area (m²)}
   \]
5. Displays biomass estimates directly on the plot

## 📁 File

- `CHL-a-Svalbard_v02.00.py`: Main script

## 🔧 Requirements

- Python 3.x
- `numpy`, `matplotlib`, `netCDF4`

Install with:

```bash
pip install numpy matplotlib netCDF4
