# Radionuclide Dataset - Construction Materials

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)

---

##  Overview

This repository contains a comprehensive dataset of natural radionuclides (\(^{226}\text{Ra}\), \(^{232}\text{Th}\), and \(^{40}\text{K}\)) in various construction materials, along with calculated radiation indices. These data were collected during the doctoral research of Leandro Barbosa da Silva, titled Radiometric Analysis of Construction Materials Commercialized in the State of Rio de Janeiro: Overview for the Implementation of Reference Values and Risk Incidence (2024) (https://www.nuclear.ufrj.br/images/undefined/Tese_Leandro_Barbosa_da_Silva.pdf). The dataset is fully processed, validated, and ready for use in scientific research, machine learning applications, and radiological safety assessments.

### Key Features

- **109 samples** across 7 material types
- **9 numerical variables** including radionuclide activities and radiation indices
- **100% data completeness** - no missing values
- **Fully validated** - no duplicate identifiers
- **Multiple formats** - CSV (ML-ready), CSV (Brazilian format), Excel
- **Reproducible preprocessing** - complete code and documentation provided

---

## Repository Structure

```
radionuclide-dataset/
│
├── data/ # Raw data (not included in Zenodo)
│ └── OriginalData.xlsx
│
├── scripts/ # Processing scripts (not included in Zenodo)
│ ├── preprocessing_.py # Main preprocessing script
│ ├── config.yaml # Configuration file
│ └── requirements.txt # Python dependencies
│
├── dataset_zenodo/ #  Complete dataset for Zenodo
│ ├── README.md # Dataset description
│ ├── dados/ # Processed data files
│ │ ├── dados_processados.csv # ML format (sep=, dec=.)
│ │ ├── dados_processados_BR.csv # Brazilian Excel format (sep=; dec=,)
│ │ └── dados_processados.xlsx # Excel format
│ ├── documentacao/ # Documentation and reports
│ │ ├── relatorio_validacao.txt # Validation report
│ │ ├── estatisticas_descritivas.csv # Descriptive statistics
│ │ └── relatorio_completo.md # Complete processing report
│ ├── figuras/ # Statistical figures
│ │ ├── distribuicao_materiais.png
│ │ ├── boxplot_radionuclideos.png
│ │ ├── matriz_correlacao.png
│ │ ├── pairplot_radionuclideos.png
│ │ ├── barras_erro_materiais.png
│ │ ├── histograma_indices.png
│ │ └── tabela_estatisticas.png
│ └── codigo/ # Code for reproducibility
│ ├── preprocessing.py
│ ├── config.yaml
│ ├── requirements.txt
│ ├── environment.yml
│ └── README.md
│
├── LICENSE # MIT License
└── README.md # This file
```  

---

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Conda (recommended) or pip

### Installation

#### Using Conda (recommended)

```bash
# Clone the repository
git clone https://github.com/NBC777/radionuclide-dataset.git
cd radionuclide-dataset

# Create and activate Conda environment
conda env create -f dataset_zenodo/codigo/environment.yml
conda activate project_cetem

pip install -r dataset_zenodo/codigo/requirements.txt

# Running the Preprocessing
python scripts/preprocessing_.py --config scripts/config.yaml
```

Loading the Data
Python (for ML/Analysis)
```python

import pandas as pd

# Load ML-ready format
df = pd.read_csv(
    'dataset_zenodo/dados/dados_processados.csv',
    sep=',',
    decimal='.'
)

# Explore the data
print(df.head())
print(df.info())
print(df.describe())
```

Excel (Brazilian Portuguese)

Open dataset_zenodo/dados/dados_processados_BR.csv in Excel (automatically recognizes ; as separator and , as decimal).
Excel (International)

Open dataset_zenodo/dados/dados_processados.xlsx directly.



## Data Description

### Sample Information

| Variable | Description | Type |
|----------|-------------|------|
| **Samples** | Sample identifier code | Categorical |
| **Material** | Material type classification | Categorical |

### Radionuclide Activities

| Variable | Description | Unit | Mean ± Std | Min | Max |
|----------|-------------|------|------------|-----|-----|
| **226Ra** | Radium-226 activity | Bq/kg | 74.98 ± 44.06 | 8.32 | 266.91 |
| **232Th** | Thorium-232 activity | Bq/kg | 68.30 ± 74.87 | 3.52 | 702.13 |
| **40K** | Potassium-40 activity | Bq/kg | 625.44 ± 325.78 | 13.87 | 1204.77 |

### Radiation Indices

| Variable | Description | Unit | Mean ± Std | Min | Max |
|----------|-------------|------|------------|-----|-----|
| **Raeq** | Radium equivalent activity | Bq/kg | 220.81 ± 141.25 | 19.01 | 1295.24 |
| **Theq** | Thorium equivalent activity | Bq/kg | 155.19 ± 98.90 | 13.32 | 906.58 |
| **Keq** | Potassium equivalent activity | Bq/kg | 2651.97 ± 1811.04 | 249.76 | 16805.86 |
| **IA** | Alpha radiation index | - | 0.37 ± 0.22 | 0.04 | 1.33 |
| **IB** | Brazilian  radiation index | - | 0.71 ± 0.42 | 0.06 | 3.77 |
| **IG** | Gamma radiation index | - | 0.80 ± 0.50 | 0.07 | 4.52 |

*Note: Full descriptive statistics available in `dataset_zenodo/documentacao/estatisticas_descritivas.csv`.*

---

## Material Classification

The dataset includes 7 material types with the following distribution:

| Code | Material Type | Samples | Percentage |
|------|---------------|---------|------------|
| AR | Comercial sand | 27 | 24.8% |
| A | Structural cement | 23 | 21.1% |  
| PB | Crushed rock | 20 | 18.3% |
| HB | Hollow ceramic / bore brick | 14 | 12.8% |
| PP | Stone dust | 10 | 9.2% |
| SB | Solid clay brick | 9 | 8.3% |
| CB | Concrete block brick | 6 | 5.5% |

---



## Calculation of Indices

The radiation indices were calculated using internationally recognized formulas (UNSCEAR, 2000; Beretka & Mathew, 1985):

### Radium Equivalent Activity (Raeq)

The radium equivalent activity is a weighted sum of the activities of ²²⁶Ra, ²³²Th, and ⁴⁰K, assuming that 370 Bq/kg of ²²⁶Ra, 259 Bq/kg of ²³²Th, and 4810 Bq/kg of ⁴⁰K produce the same gamma dose rate.

```math
Raeq = ARa + 1.43 × ATh + 0.077 × AK
```

### Thorium Equivalent Activity (Theq)

The thorium equivalent activity represents the contribution of thorium to the total radiation dose.

```math
Theq = ATh + 0.7 × ARa + 0.045 × AK
```

### Potassium Equivalent Activity (Keq)

The potassium equivalent activity represents the contribution of potassium to the total radiation dose.

```math 
Keq = AK + 13 × ARa + 10 × ATh
```

###  Alpha Radiation  Index (IA)

The activity concentration index is used to assess the radiological risk from building materials, with a recommended limit of IA ≤ 1 for materials used in bulk quantities.

```math 
IA = ARa/300 + ATh/200 + AK/3000
```

### Brazilian Radiation Index (IB)

The Brazilian radiation index is used to assess the external gamma radiation hazard, with a recommended limit of IB ≤ 1.

```math
IB = ARa/370 + ATh/259 + AK/4810
```

### Gamma  Radiation Index (IG)

The internal radiation index accounts for both external and internal exposure, with a recommended limit of IG ≤ 1.

```math
IG = ARa/185 + ATh/259 + AK/4810
```

Where:

    - ARa = Activity of ²²⁶Ra (Bq/kg)

    - ATh = Activity of ²³²Th (Bq/kg)

    - AK = Activity of ⁴⁰K (Bq/kg)


##  Applications

### Scientific Research

- Radiological safety assessment of building materials
- Comparative studies of radionuclide concentrations
- Environmental radioactivity monitoring
- Health physics and radiation protection

### Machine Learning & AI

- **Generative Adversarial Networks (GANs)**: Generate synthetic radionuclide data for data augmentation
- **Regression Models**: Predict radiation indices from activities
- **Classification**: Identify material types based on radionuclide signatures
- **Dimensionality Reduction**: PCA, t-SNE, UMAP for feature analysis
- **Anomaly Detection**: Identify unusual radionuclide patterns

### Industrial Applications

- Quality control in construction material production
- Regulatory compliance testing
- Supply chain material screening
- Building certification and safety assessments

---

## Quality Assurance

The dataset has undergone rigorous validation:

| Quality Check | Status |
|---------------|--------|
| Missing values | 0 missing (100% complete) |
| Duplicate samples | 0 duplicates |
| Data consistency | All numerical values properly typed |
| Material classification | All samples categorized |
| Reproducibility | Complete code provided |
| Documentation | Full documentation available |

---

## Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{barbosa_baygorrea_2026_radionuclide,
  author       = {Leandro Barbosa and Nancy Baygorrea},
  title        = {Radionuclide Dataset for Construction Materials},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {1.0},    
  doi          = {10.5281/zenodo.21348303},
  url          = {https://doi.org/10.5281/zenodo.21348303}
}
```

##  Authors and Acknowledgments

### Authors

| Author | Contribution |
|--------|--------------|
| **Leandro Barbosa^{1}** | Data collection and research |
| **Nancy Baygorrea** | Preprocessing and documentation |

---

### Institutional Support

**^{1}** Laboratory of Simulation and Nuclear Physics  
Federal University of Rio de Janeiro (UFRJ)

---

### Funding

**^{1}** This research was supported by the **Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)**  
Grant/Protocol Number: [XXXXX]

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**You are free to:**
-  Use the data for any purpose
-  Modify and adapt the data
-  Share and redistribute
-  Use in commercial applications

**Under the condition:**
-  Provide attribution to the original authors

---

##  References

1. Beretka, J., & Mathew, P. J. (1985). Natural radioactivity of Australian building materials, industrial wastes and by-products. *Health Physics*, 48(1), 87-95.

2. United Nations Scientific Committee on the Effects of Atomic Radiation (UNSCEAR). (2000). *Sources and Effects of Ionizing Radiation*. UNSCEAR Report to the General Assembly.

3. European Commission. (1999). *Radiological Protection Principles Concerning the Natural Radioactivity of Building Materials*. Radiation Protection 112.


