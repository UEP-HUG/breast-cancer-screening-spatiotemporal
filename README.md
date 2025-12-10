# Spatiotemporal dynamics of breast cancer screening across half a million invitations in Geneva, Switzerland

## Authors

**David De Ridder**<sup>1,2,3,4</sup>, **Béatrice Arzel**<sup>5</sup>, **Stéphane Joost**<sup>1,2,3,6</sup>, **Idris Guessous**<sup>1,2,3,4,°</sup>

<sup>1</sup>Geographic Information Research and Analysis in Population Health (GIRAPH) Lab, Faculty of Medicine, University of Geneva (UNIGE), Geneva, Switzerland
<sup>2</sup>Geospatial Molecular Epidemiology (GEOME), Laboratory of Biologic Geochemistry, School of Architecture, Civil and Environmental Engineering (ENAC), École Polytechnique Fédérale de Lausanne (EPFL), Lausanne, Switzerland
<sup>3</sup>Division and Department of Primary Care Medicine, Geneva University Hospitals, Geneva, Switzerland
<sup>4</sup>Faculty of Medicine, University of Geneva, Geneva, Switzerland
<sup>5</sup>Fondation genevoise pour le dépistage du cancer, Geneva, Switzerland
<sup>6</sup>La Source School of Nursing, University of Applied Sciences and Arts Western Switzerland (HES-SO), 1004 Lausanne, Switzerland

<sup>°</sup>Corresponding author: Professor Idris Guessous, MD, PhD
Email: [Idris.Guessous@hug.ch](mailto:Idris.Guessous@hug.ch)
Address: Rue Gabrielle Perret Gentil 4, 1205 Geneva, Switzerland
Phone: +41 (0)22 305 58 61

## Project Description

This repository contains the code and analysis pipeline for a comprehensive spatiotemporal analysis of breast cancer screening participation in Geneva, Switzerland. The study examines over half a million screening invitations to understand geographic and temporal patterns in mammography screening uptake.

The analysis combines:
- **Geocoding** of participant addresses using Swiss Federal address databases
- **Spatial accessibility analysis** to screening centers using road network data
- **Socioeconomic deprivation indices** at the neighborhood level
- **Spatiotemporal clustering** and hot spot analysis
- **Neighborhood-level analyses** of screening participation patterns

## Repository Structure

```
GIRACS/
├── Data/
│   ├── Raw data/          # Original screening invitation data
│   ├── Processed data/    # Geocoded and processed datasets
│   └── Misc data/         # Administrative boundaries, road networks
├── Scripts/
│   ├── 1. Data preparation.ipynb           # Data cleaning, geocoding, accessibility
│   ├── 2. Analyses - Neighborhood.ipynb    # Spatial analyses and clustering
│   ├── utils.py                            # Utility functions for mapping
│   └── Archives/                           # Archived analysis scripts
├── Results/
│   ├── Cluster analyses/                   # Clustering results and figures
│   └── Local Autocorrelation/              # Getis-Ord Gi* spatial statistics
├── Manuscript/                             # Manuscript files and figures
└── Miscellaneous/                          # Additional documentation
```

## Data

### Raw Data
- **extractionGE.csv**: Breast cancer screening invitation data from the Geneva Foundation for Cancer Screening (FGDC)
- Contains information on:
  - Invitation and screening dates
  - Participant addresses
  - Age groups (50-74 years)
  - Screening outcomes

### Processed Data
- **Geocoded addresses**: ~98% successfully geocoded to building-level precision
- **Accessibility metrics**: Distance to nearest screening centers
- **Neighborhood characteristics**: Socioeconomic deprivation indices from Swiss MicroGIS data
- **Median income**: Sous-secteur level income data (2005-2016)

### Study Population
- **Total invitations**: 581,325 (after quality filtering)
- **Unique women**: 135,203
- **Study period**: 1999-2020
- **Age range**: 50-74 years
- **Geographic coverage**: Canton of Geneva, Switzerland

## Analysis Pipeline

### 1. Data Preparation (`1. Data preparation.ipynb`)

**Key steps:**
1. **Data import and cleaning**
   - Import screening invitation records from FGDC
   - Clean and standardize address fields
   - Handle missing data and duplicates

2. **Geocoding**
   - Match addresses to Swiss Federal RegBL database
   - Achieve ~98% geocoding success rate at building level
   - Spatial projection to Swiss coordinate system (EPSG:2056)

3. **Accessibility analysis**
   - Calculate distance to nearest screening centers
   - Use Pandana for network-based accessibility metrics
   - Compute screening center density within 5km radius

4. **Socioeconomic variables**
   - Create neighborhood-level deprivation index using PCA
   - Variables: education, income, unemployment, foreign nationals, ...

5. **Quality filtering**
   - Exclude invitations outside age guidelines
   - Remove addresses outside Canton of Geneva
   - Final dataset: 579,033 invitations

### 2. Neighborhood-Level Analyses (`2. Analyses - Neighborhood.ipynb`)

**Spatial analyses:**
- Hot spot analysis using Getis-Ord Gi* statistics
- Spatiotemporal clustering of participation patterns
- Emerging hot spot analysis over time
- Spatial autocorrelation assessment
- Hierarchical clustering of neighborhoods

### 3. Utility Functions (`utils.py`)

**Provides:**
- Mapping functions for spatial visualization
- Custom color schemes for choropleth maps
- Statistical plotting utilities
- Translation functions for multilingual outputs

## Key Methods

### Geocoding
- Custom geocoding pipeline using Swiss Federal RegBL address database
- String matching algorithms for address standardization
- Fallback to street-level geocoding when building match unavailable

### Accessibility Metrics
- Road network from OpenStreetMap via OSMnx
- Network-based distance calculations using Pandana
- Screening center locations from FGDC records

### Deprivation Index
Principal Component Analysis on:
- % foreign nationals
- Inverse median income
- % unemployed
- % without tertiary education
- Inverse median rent
- % with primary/secondary education only

### Spatial Statistics
- Getis-Ord Gi* for hot spot detection
- Spatial weights matrices (600m distance threshold)
- Emerging hot spot analysis for temporal patterns
- Local Indicators of Spatial Association (LISA)

## Requirements

### Python Packages
```python
pandas >= 1.3.0
numpy >= 1.21.0
geopandas >= 0.10.0
shapely >= 1.8.0
osmnx >= 1.1.0
pandana >= 0.6.0
libpysal >= 4.5.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
mapclassify >= 2.4.0
scikit-learn >= 1.0.0
statsmodels >= 0.13.0
contextily >= 1.2.0
matplotlib-scalebar >= 0.8.0
sqlalchemy >= 1.4.0
```

### Additional Requirements
- PostgreSQL database (for MicroGIS data)
- Swiss Federal RegBL address database
- OpenStreetMap network data

## Usage

1. **Set up environment:**
   ```bash
   conda create -n giracs python=3.11
   conda activate giracs
   # Install required packages
   ```

2. **Prepare data:**
   - Place raw screening data in `Data/Raw data/`
   - Ensure access to Swiss RegBL database
   - Configure PostgreSQL connection in notebooks

3. **Run analysis pipeline:**
   ```bash
   jupyter notebook
   # Open and run notebooks in sequence:
   # 1. Data preparation.ipynb
   # 2. Analyses - Neighborhood.ipynb
   ```

4. **Output:**
   - Processed datasets saved to `Data/Processed data/`
   - Figures and results exported to `Results/`

## Key Findings

The analysis reveals:
- Significant spatial clustering of screening participation
- Persistent hot spots in affluent neighborhoods
- Cold spots in areas with higher socioeconomic deprivation
- Temporal evolution of participation patterns
- Impact of screening center accessibility on participation

## Citation

If you use this code or data, please cite:

```
De Ridder, D., Arzel, B., Joost, S., & Guessous, I. (2025).
Spatiotemporal dynamics of breast cancer screening across half a million invitations
in Geneva, Switzerland. [Journal details to be added upon publication]
```

## License

[To be determined - please specify your preferred license]

## Contact

For questions or collaborations:
- **David De Ridder**: [David.deridder@hug.ch](mailto:David.deridder@hug.ch)
- **Prof. Idris Guessous**: [Idris.Guessous@hug.ch](mailto:Idris.Guessous@hug.ch)

## Acknowledgments

We acknowledge:
- The Geneva Foundation for Cancer Screening (FGDC) for providing the screening data
- The Swiss Federal Statistical Office for RegBL address data
- The SITG (Système d'Information du Territoire à Genève) for geographic data
- Study participants who contributed to this research

## Data Availability

Due to privacy regulations, individual-level screening data cannot be publicly shared.
Aggregated neighborhood-level results are available in the `Results/` folder.

---

**Last updated**: December 2025
**Repository maintained by**: David De Ridder, GIRAPH Lab, Geneva University Hospitals
