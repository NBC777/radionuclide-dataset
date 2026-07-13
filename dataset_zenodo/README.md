# Radionuclide Dataset - Construction Materials

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

---

## Dataset Overview

This dataset contains measurements of natural radionuclides (²²⁶Ra, ²³²Th, and ⁴⁰K) in various construction materials, along with calculated radiation indices. The data has been fully processed, validated, and is ready for use in scientific research, machine learning applications, and radiological safety assessments.

### Key Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | 109 |
| **Material Types** | 7 |
| **Variables** | 11 (2 categorical, 9 numerical) |
| **Completeness** | 100% (no missing values) |
| **Data Quality** | Fully validated, no duplicates |

---

## Files Included

### Data Files (`/dados/`)

| File | Format | Separator | Decimal | Use Case |
|------|--------|-----------|---------|----------|
| `dados_processados.csv` | CSV | `,` (comma) | `.` (dot) | Machine Learning, Python analysis |
| `dados_processados_BR.csv` | CSV | `;` (semicolon) | `,` (comma) | Excel (Brazilian/Portuguese) |
| `dados_processados.xlsx` | Excel | - | - | General visualization |

### Documentation (`/documentacao/`)

| File | Description |
|------|-------------|
| `relatorio_validacao.txt` | Data validation report |
| `estatisticas_descritivas.csv` | Complete descriptive statistics |
| `relatorio_completo.md` | Detailed processing report |

### Figures (`/figuras/`)

| File | Description |
|------|-------------|
| `distribuicao_materiais.png` | Material type distribution |
| `boxplot_radionuclideos.png` | Radionuclide distributions by material |
| `matriz_correlacao.png` | Correlation matrix heatmap |
| `pairplot_radionuclideos.png` | Relationships between main variables |
| `barras_erro_materiais.png` | Mean activities with error bars |
| `histograma_indices.png` | Radiation indices distributions |
| `tabela_estatisticas.png` | Statistical summary table |

### Code (`/codigo/`)

Complete code for data preprocessing and reproducibility. See `codigo/README.md` for details.

---

## Variables Description

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

*Note: Full descriptive statistics available in `documentacao/estatisticas_descritivas.csv`.*

---

##  Material Classification

The dataset includes 7 material types with the following distribution:

| Code | Material Type | Samples | Percentage |
|------|---------------|---------|------------|
| C. Sand | Comercial sand | 27 | 24.8% |
| S. Cem | Structural cement | 23 | 21.1% |
| PB | Crushed rock | 20 | 18.3% |
| CB | Hollow ceramic / bore brick | 14 | 12.8% |
| PP | Stone dust | 10 | 9.2% |
| SB | Solid clay brick | 9 | 8.3% |
| CB | Concrete block brick | 6 | 5.5% |

---

##  Calculation of Indices

The radiation indices were calculated using internationally recognized formulas:

### Radium Equivalent Activity (Raeq)
```math
Raeq = ARa + 1.43 × ATh + 0.077 × AK
```

### Thorium Equivalent Activity (Theq)
```math
Theq = ATh + 0.7 × ARa + 0.045 × AK
```

### Potassium Equivalent Activity (Keq)
```math
Keq = AK + 13 × ARa + 10 × ATh
```

###  Activity Concentration Index (IA)
```math

IA = ARa/300 + ATh/200 + AK/3000
```

### External Radiation Index (IB)
```math
IB = ARa/370 + ATh/259 + AK/4810
```

### Internal Radiation Index (IG)
```math
IG = ARa/185 + ATh/259 + AK/4810
```

Where:
```math
    ARa = Activity of ²²⁶Ra (Bq/kg)

    ATh = Activity of ²³²Th (Bq/kg)

    AK = Activity of ⁴⁰K (Bq/kg)

```

---

###  Citation

If you use this dataset in your research, please cite:

@phdthesis{leandro_2024_radionuclide,
  author       = {Leandro Barbosa da Silva},
  title        = {ANÁLISE RADIOMÉTRICA DE MATERIAIS DE CONSTRUÇÃO
COMERCIALIZADOS NO ESTADO DO RIO DE JANEIRO: LEVANTAMENTO DE
UM PANORAMA GERAL PARA IMPLEMENTAÇÃO DE VALORES DE
REFERÊNCIA E INCIDÊNCIA DE RISCOS},
  year         = {2024},
  address      = {Rio de Janeiro},
  month        = {november},
  note         = {Doctoral dissertation},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://www.nuclear.ufrj.br/images/undefined/Tese_Leandro_Barbosa_da_Silva.pdf}
}

@dataset{nancy_2026_radionuclide,
  author       = {Nancy, [Full Name]},
  title        = {Radionuclide Dataset for Construction Materials},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {1.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX}
}

---

# Authors and Acknowledgments

### Authors
1. **Leandro Barbosa da Silva** 
   Data collection and research  
   Laboratory of Simulation and Nuclear Physics  
   Federal University of Rio de Janeiro (UFRJ)
   **Laboratory of Simulation and Nuclear Physics**  
   Federal University of Rio de Janeiro (UFRJ)

	- Funding: **Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq)**: Grant/Protocol Number: [XXXXX]

2. **Nancy Baygorrea**  
   Preprocessing and documentation  
   Dataset organization and validation
   State University of Northern Rio de Janeiro (UENF)
   Laboratory of Mathematical Sciences (LCMAT)
   

### Contributions
- **Leandro Barbosa**: Research design, data collection, experimental measurements, sample preparation
- **Nancy Baygorrea**: Data preprocessing, validation, documentation, dataset organization, figure generation



---

### Acknowledgments

We gratefully acknowledge:

    The Laboratory of Simulation and Nuclear Physics for providing the infrastructure

    CNPq for the financial support

    All collaborators who contributed to sample collection and analysis

---

### License

This dataset is licensed under the MIT License.

You are free to:

    -  Use the data for any purpose

    - Modify and adapt the data

    - Share and redistribute

    - Use in commercial applications

Under the condition:

    - Provide attribution to the original authors
    
Este código é parte do dataset disponível no Zenodo.


See the LICENSE file for full terms.
Contact

Leandro Silva
Laboratório de Simulação e Física Nuclear
Universidade Federal do Rio de Janeiro (UFRJ)
Email: [leandro.silva@ufrj.br]
[ORCID: 0000-0000-0000-0000]

Dataset Repository:
[GitHub Repository URL]
[Zenodo Repository URL]


### References

    - United Nations Scientific Committee on the Effects of Atomic Radiation (UNSCEAR). (2000). Sources and Effects of Ionizing Radiation. UNSCEAR Report to the General Assembly.

    - International Atomic Energy Agency (IAEA). (2003). Guidelines for Radioelement Mapping Using Gamma Ray Spectrometry Data. IAEA-TECDOC-1363.

    - European Commission. (1999). Radiological Protection Principles Concerning the Natural Radioactivity of Building Materials. Radiation Protection 112.

    - Beretka, J., & Mathew, P. J. (1985). Natural radioactivity of Australian building materials, industrial wastes and by-products. Health Physics, 48(1), 87-95.

    - Silva, L. (2026).ANÁLISE RADIOMÉTRICA DE MATERIAIS DE CONSTRUÇÃO COMERCIALIZADOS NO ESTADO DO RIO DE JANEIRO: LEVANTAMENTO DE UM PANORAMA GERAL PARA IMPLEMENTAÇÃO DE VALORES DE REFERÊNCIA E INCIDÊNCIA DE RISCOS. PhD Thesis, Universidade Federal do Rio de Janeiro. [https://www.nuclear.ufrj.br/images/undefined/Tese_Leandro_Barbosa_da_Silva.pdf]

    - United Nations Scientific Committee on the Effects of Atomic Radiation (UNSCEAR). (2008). Sources and Effects of Ionizing Radiation. UNSCEAR Report to the General Assembly.
    
---

### Version History
Version	Date	Changes
1.0	2026-07-12	Initial release

Last Updated: 2026-07-12
Version: 1.0
Status:  Active - Ready for Use



        
