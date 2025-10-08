# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python project for generating wind roses and frequency tables from oceanographic data. The main functionality is contained in `script.py` which processes Excel files containing directional and value data (like wave direction/period or current direction/speed) and generates both polar visualizations (wind roses) and statistical frequency tables.

## Common Commands

### Running the Analysis
```powershell
# Run the main script with default configurations
python script.py

# Run the script and save outputs
python script.py
```

The script will generate:
- PNG files with wind rose visualizations
- Excel files with frequency tables
- Display interactive plots

### Dependencies
The project requires these Python packages:
- pandas (for data processing)
- matplotlib (for plotting)
- numpy (for numerical operations)

Install dependencies:
```powershell
pip install pandas matplotlib numpy openpyxl
```

## Code Architecture

### Main Function: `generar_rosa_vientos()`
The core function that orchestrates the entire process:
1. Reads Excel data using pandas
2. Validates column existence
3. Processes directional data into 16-sector compass directions (N, NNE, NE, etc.)
4. Creates value ranges using pd.cut()
5. Generates frequency crosstabs
6. Creates dual subplot visualization (wind rose + frequency table)
7. Exports results to PNG and Excel formats

### Visualization Functions
- `crear_rosa_vientos()`: Creates polar plot with stacked bars representing value ranges across directional sectors
- `crear_tabla_frecuencias()`: Renders frequency data as a formatted table subplot

### Data Processing Approach
The script uses a 16-sector directional binning system with cardinal and intercardinal directions. It converts degrees to radians, handles 360-degree wrapping, and creates polar histograms with customizable value ranges.

### Configuration Pattern
The script uses dictionary-based configuration objects that specify:
- Excel file paths
- Column names for direction and value data
- Value range bins
- Output file naming

## Input Data Format

The script expects Excel files with columns containing:
- Directional data (in degrees, 0-360)
- Value data (numerical, will be binned into ranges)

Current examples process:
- Wave data: Peak direction vs Peak period
- Current data: Direction vs Speed at different depths

## Output Files

For each analysis run, the script generates:
- `{nombre_salida}.png`: Combined wind rose and frequency table visualization
- `{nombre_salida}_tabla_frecuencias.xlsx`: Detailed frequency statistics

## Development Notes

- The polar plot is configured with North at top and clockwise direction
- Uses viridis colormap for value range visualization
- Frequency tables show percentages rounded to 2 decimal places
- Default DPI is 300 for high-quality output images