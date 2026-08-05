# Radionuclide Dataset – Construction Materials

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)

---

## Overview

This repository provides a curated dataset of natural radionuclides (${}^{226}\text{Ra}$, ${}^{232}\text{Th}$ and ${}^{40} \text{K}$) in construction materials, together with derived radiation indices. The data were collected during the doctoral research of **Leandro Barbosa da Silva**, titled:

> *Radiometric Analysis of Construction Materials Commercialized in the State of Rio de Janeiro: Overview for the Implementation of Reference Values and Risk Incidence* (2024)  
> (https://www.nuclear.ufrj.br/images/undefined/Tese_Leandro_Barbosa_da_Silva.pdf)

The dataset is fully processed, validated and ready for use in scientific research, machine learning applications and radiological safety assessments.

### Key features

- **109 samples** across 7 material types  
- **9 numerical variables** including radionuclide activities and radiation indices  
- **100% data completeness** (no missing values)  
- **Fully validated** (no duplicate identifiers)  
- **Multiple formats**: CSV (ML-ready), CSV in Brazilian format, Excel  
- **Reproducible preprocessing**: complete code and documentation provided  

---

## Repository structure

```text
radionuclide-dataset/
│
├── data/                   # Raw data (not included in Zenodo)
│   └── OriginalData.xlsx
│
├── scripts/                # Processing scripts (not included in Zenodo)
│   ├── preprocessing_.py   # Main preprocessing script
│   ├── config.yaml         # Configuration file
│   └── requirements.txt    # Python dependencies
│
├── dataset_zenodo/         # Complete dataset for Zenodo
│   ├── README.md           # Dataset-level description
│   ├── dados/              # Processed data files
│   │   ├── dados_processados.csv      # ML format (sep=',' dec='.')
│   │   ├── dados_processados_BR.csv   # Brazilian Excel format (sep=';' dec=',')
│   │   └── dados_processados.xlsx     # Excel format
│   ├── documentacao/       # Documentation and reports
│   │   ├── relatorio_validacao.txt    # Validation report
│   │   ├── estatisticas_descritivas.csv # Descriptive statistics
│   │   └── relatorio_completo.md      # Complete processing report
│   ├── figuras/            # Statistical figures
│   │   ├── distribuicao_materiais.png
│   │   ├── boxplot_radionuclideos.png
│   │   ├── matriz_correlacao.png
│   │   ├── pairplot_radionuclideos.png  
│   │   ├── barras_erro_materiais.png
│   │   ├── histograma_indices.png
│   │   └── tabela_estatisticas.png
│   └── codigo/             # Code for reproducibility
│       ├── preprocessing.py
│       ├── config.yaml
│       ├── requirements.txt
│       ├── environment.yml
│       └── README.md
│
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## Quick start

### Prerequisites

- Python 3.10 or higher  
- Conda (recommended) or pip  

### Installation

Using Conda (recommended):

```bash
# Clone the repository
git clone https://github.com/NBC777/radionuclide-dataset.git
cd radionuclide-dataset

# Create and activate the Conda environment
conda env create -f dataset_zenodo/codigo/environment.yml
conda activate project_cetem

# Install Python dependencies
pip install -r dataset_zenodo/codigo/requirements.txt

# Run preprocessing (if you want to reproduce the pipeline)
python scripts/preprocessing_.py --config scripts/config.yaml
```

### Loading the data

Python (for ML and analysis):

```python
import pandas as pd

# Load ML-ready format
df = pd.read_csv(
    "dataset_zenodo/dados/dados_processados.csv",
    sep=",",
    decimal="."
)

# Explore the data
print(df.head())
print(df.info())
print(df.describe())
```

Excel (Brazilian Portuguese):

- Open `dataset_zenodo/dados/dados_processados_BR.csv` in Excel.  
- Excel will automatically recognize `;` as separator and `,` as decimal symbol.

Excel (International):

- Open `dataset_zenodo/dados/dados_processados.xlsx` directly.

---

## Data description

### Sample information

| Variable  | Description                  | Type        |
|----------|------------------------------|-------------|
| Samples  | Sample identifier code       | Categorical |
| Material | Material type classification | Categorical |

### Radionuclide activities


| Variable | Description           | Unit  | Mean $\pm$ Std      | Min   | Max    |
|----------|-----------------------|-------|-----------------|-------|--------|
| ${}^{226}\text{Ra}$   | Radium-226 activity   | Bq/kg | 74.98 $\pm$ 44.06   | 8.32  | 266.91 |
| ${}^{232}\text{Th}$    | Thorium-232 activity  | Bq/kg | 68.30 $\pm$ 74.87   | 3.52  | 702.13 |
| ${}^{40} \text{K}$      | Potassium-40 activity | Bq/kg | 625.44 $\pm$ 325.78 | 13.87 | 1204.77|

### Radiation indices

| Variable | Description                     | Unit  | Mean $\pm$ Std        | Min   | Max      |
|----------|---------------------------------|-------|-------------------|-------|----------|
| $\text{Ra}_\text{eq}$     | Radium equivalent activity      | Bq/kg | 220.81 $\pm$ 141.25   | 19.01 | 1295.24  |
| $\text{Th}_\text{eq}$     | Thorium equivalent activity     | Bq/kg | 155.19 $\pm$ 98.90    | 13.32 | 906.58   |
| $\text{K}_\text{eq}$      | Potassium equivalent activity   | Bq/kg | 2651.97 $\pm$ 1811.04 | 249.76| 16805.86 |
| $\text{I}_\text{A}$       | Alpha radiation index           | –     | 0.37 $\pm$ 0.22       | 0.04  | 1.33     |
| $\text{I}_\text{B}$       | Brazilian radiation index       | –     | 0.71 $\pm$ 0.42       | 0.06  | 3.77     |
| $\text{I}_\text{G}$       | Gamma radiation index           | –     | 0.80 $\pm$ 0.50       | 0.07  | 4.52     |

Full descriptive statistics are available in `dataset_zenodo/documentacao/estatisticas_descritivas.csv`.

---

### Exploratory statistical analysis

A comprehensive exploratory statistical analysis of the dataset is provided as a PDF report in `dataset_zenodo/documentacao/analise_exploratoria_dataset.pdf`. 
It includes distribution plots by material type, correlation analysis, boxplots, histograms of radionuclide activities and indices, and extended summary tables.

---
## Material classification

The dataset includes 7 material types with the following distribution:

| Code | Material type                   | Samples | Percentage |
|------|---------------------------------|---------|-----------|
| AR   | Commercial sand                 | 27      | 24.8%     |
| A    | Structural cement               | 23      | 21.1%     |
| PB   | Crushed rock                    | 20      | 18.3%     |
| HB   | Hollow ceramic / bore brick     | 14      | 12.8%     |
| PP   | Stone dust                      | 10      | 9.2%      |
| SB   | Solid clay brick                | 9       | 8.3%      |
| CB   | Concrete block brick            | 6       | 5.5%      |

---

## Calculation of indices

The radiation indices were calculated using internationally recognized formulas (UNSCEAR, 2000; Beretka & Mathew, 1985).

> **Note:** The $\text{Ra}_\text{eq}$ formula below is standard in the literature. The definitions of $\text{Th}_\text{eq}$, $\text{K}_\text{eq}$, $\text{I}_\text{A}$, $\text{I}_\text{B}$ and $\text{I}_\text{G}$ follow the conventions adopted in the underlying doctoral work and Brazilian practice; they may not coincide exactly with all international standards, so users should consult the thesis for formal derivations.

### Radium equivalent activity ($\text{Ra}_\text{eq}$)

$\text{Ra}_\text{eq}$ is a weighted sum of the activities of ${}^{226}\text{Ra}$, ${}^{232}\text{Th}$ and ${}^{40} \text{K}$, under the assumption that 370 Bq/kg of ${}^{226} \text{Ra}$, 259 Bq/kg of ${}^{232} \text{Th}$ and 4810 Bq/kg of ${}^{40} \text{K}$ produce comparable gamma dose rates.

```text
$\text{Ra}_\text{eq}$ = A $\text{Ra}$ + 1.43 \times A $\text{Th}$ + 0.077 \times A $\text{K}$
```

### Thorium equivalent activity ($\text{Th}_\text{eq}$)

Theq represents the contribution of thorium to the total radiation dose, expressed as an equivalent activity combining ${}^{232} \text{Th}$, ${}^{226} \text{Ra}$ and ${}^{40}\text{K}$:

```text
Theq = $A \, \text{Th}$ + 0.7 \times $A \, \text{Ra}$ + 0.045 \times $A \, \text{K}$
```

### Potassium equivalent activity (Keq)

Keq represents the contribution of potassium to the total radiation dose, expressed as an equivalent activity combining ${}^{40} \text{K}$, ${}^{226} \text{Ra}$ and ${}^{232} \text{Th}$:

```text
$\text{K}_\text{eq}$ = $A \, \text{K}$ + 13 \times $A \, \text{Ra}$ + 10 \times $A \, \text{Th}$
```

### Alpha radiation index (IA)

IA is an activity concentration index used to assess radiological risk from building materials, with a recommended limit of $\text{I}_\text{A} \leq 1 $ for materials used in bulk quantities:

```text
$\text{I}_\text{A}$ = $A \, \text{Ra}$ / 300 + $A \, \text{Th}$ / 200 + $A \, \text{K}$ / 3000
```

### Brazilian radiation index ($\text{I}_\text{B}$)

$\text{I}_\text{B}$ is a composite index used in Brazilian practice to assess the external gamma radiation hazard, with a recommended limit of $\text{I}_\text{B} \leq 1$:

```text
$\text{I}_\text{B}$ = $A \, \text{Ra}$ / 370 + $A \, \text{Th}$ / 259 + $A \, \text{K}$ / 4810
```

### Gamma radiation index ($\text{I}_\text{G}$)

$\text{I}_\text{G}$ is an index designed to account for gamma exposure, with a recommended limit of $\text{I}_\text{G} \leq  1$:

```text
$\text{I}_\text{G}$ = $A \, \text{Ra}$ / 185 + $A \, \text{Th}$ / 259 + $A \, \text{K}$ / 4810
```
$\text{I}_\text{G}$ = $A \, \text{Ra}$ / 185 + $A \, \text{Th}$ / 259 + $A \, \text{K}$ / 4810


Where:

- $A  \text{Ra}$ = activity of ${}^{226} \text{Ra}$ (Bq/kg)  
- $A  \text{Th}$ = activity of ${}^{232} \text{Th}$ (Bq/kg)  
- $A  \text{K}$  = activity of ${}^{40} \text{K}$ (Bq/kg)  

---

## Applications

### Scientific research

- Radiological safety assessment of building materials  
- Comparative studies of radionuclide concentrations  
- Environmental radioactivity monitoring  
- Health physics and radiation protection  

### Machine learning and AI

- Generative models (GANs, VAEs, flows): synthetic data generation and augmentation  
- Regression models: prediction of radiation indices from activities  
- Classification: material-type identification from radionuclide signatures  
- Dimensionality reduction (PCA, t-SNE, UMAP) for feature analysis  
- Anomaly detection: identification of unusual radionuclide patterns  

### Industrial applications

- Quality control in construction material production  
- Regulatory compliance testing  
- Material screening in supply chains  
- Building certification and safety assessments  

---

## Quality assurance

The dataset has been subjected to rigorous validation:

| Quality check           | Status                        |
|-------------------------|-------------------------------|
| Missing values          | 0 missing (100% complete)     |
| Duplicate samples       | 0 duplicates                  |
| Data consistency        | All numerical values typed    |
| Material classification | All samples categorized       |
| Reproducibility         | Complete code provided        |
| Documentation           | Full documentation available  |

---

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{barbosa_baygorrea_2026_radionuclide,
  author    = {Leandro Barbosa and Nancy Baygorrea},
  title     = {Radionuclide Dataset for Construction Materials},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.0},
  doi       = {10.5281/zenodo.21348303},
  url       = {https://doi.org/10.5281/zenodo.21348303}
}
```

---

## Authors and acknowledgments

### Authors

| Author               | Contribution                      |
|----------------------|-----------------------------------|
| **Leandro Barbosa¹** | Data collection and primary study |
| **Nancy Baygorrea**  | Preprocessing and documentation   |

### Institutional support

¹ Laboratory of Simulation and Nuclear Physics  
Federal University of Rio de Janeiro (UFRJ)

### Funding

¹ This research was supported by the **Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)**.  
Grant/Protocol Number: [XXXXX].

---

## License

This project is licensed under the MIT License – see the `LICENSE` file for details.

You are free to:

- Use the data for any purpose  
- Modify and adapt the data  
- Share and redistribute  
- Use the data in commercial applications  

Under the condition that you:

- Provide appropriate attribution to the original authors  

---

## References

1. Beretka, J., & Mathew, P. J. (1985). Natural radioactivity of Australian building materials, industrial wastes and by-products. *Health Physics*, 48(1), 87–95.  
2. United Nations Scientific Committee on the Effects of Atomic Radiation (UNSCEAR). (2000). *Sources and Effects of Ionizing Radiation*. Report to the General Assembly.  
3. European Commission. (1999). *Radiological Protection Principles Concerning the Natural Radioactivity of Building Materials*. Radiation Protection 112.