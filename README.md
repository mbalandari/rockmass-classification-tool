# Rock Mass Classification Tool

A desktop engineering application for preliminary rock-mass classification using **Rock Mass Rating (RMR)**, the **NGI Q-System**, and **Geological Strength Index (GSI)**. The application provides a PySide6 graphical interface, Matplotlib visualizations, and PDF, DOCX, and TXT report generation.

> **Engineering-use notice:** This software implements simplified classification and support-recommendation logic for engineering assessment and educational/research use. Classification outputs and support recommendations must be reviewed by a qualified geotechnical or rock-mechanics professional and should not be treated as a substitute for site investigation, engineering judgment, or project-specific design.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

## Contents

- [Rock Mass Classification Tool](#rock-mass-classification-tool)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Features](#features)
    - [Rock-mass classification](#rock-mass-classification)
    - [Visualization](#visualization)
    - [Reporting](#reporting)
  - [Methods implemented](#methods-implemented)
    - [RMR](#rmr)
    - [Q-System](#q-system)
    - [GSI](#gsi)
    - [Support recommendation](#support-recommendation)
  - [Application workflow](#application-workflow)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Windows](#windows)
    - [Linux / macOS](#linux--macos)
  - [Running the application](#running-the-application)
  - [Using the GUI](#using-the-gui)
    - [RMR categories](#rmr-categories)
    - [GSI categories](#gsi-categories)
  - [Outputs and reports](#outputs-and-reports)
    - [PDF](#pdf)
    - [DOCX](#docx)
    - [TXT](#txt)
  - [Project structure](#project-structure)
  - [Python API](#python-api)
    - [RMR](#rmr-1)
    - [Q-System](#q-system-1)
    - [GSI](#gsi-1)
    - [Support](#support)
  - [Testing](#testing)
  - [Documentation](#documentation)
  - [Engineering scope and limitations](#engineering-scope-and-limitations)
  - [Development](#development)
  - [License](#license)

## Overview

The Rock Mass Classification Tool separates the application into a GUI layer, calculation models, engineering calculation modules, plotting utilities, and report generators.

The current implementation calculates:

- **RMR** from UCS, RQD, joint spacing, joint condition, groundwater, and orientation adjustment.
- **Q-System** from RQD, Jn, Jr, Ja, Jw, and SRF.
- **GSI** from a structure category and surface-condition adjustment. A weathering value is captured in the model but is not currently used in the numerical GSI calculation.
- **Support recommendations** from Q using a simplified threshold-based rule set.

The application combines these outputs into a `ClassificationResult`, displays the headline results in the GUI, and can generate reports containing the numerical breakdowns and charts.

## Features

### Rock-mass classification

- RMR calculation with component-by-component score breakdown.
- Q-System calculation using the standard multiplicative form:

  `Q = (RQD / Jn) × (Jr / Ja) × (Jw / SRF)`

- GSI estimation from the implemented structure lookup and surface-condition adjustment.
- Simplified Q-based support recommendation output.

### Visualization

- RMR contribution bar chart.
- Q-System radar chart.
- GSI structure-domain diagram with the calculated value marked.
- PNG chart generation for report assembly.

### Reporting

Reports can be exported from the GUI in:

- PDF
- DOCX
- TXT

PDF and DOCX reports include the classification breakdowns and generated RMR, Q, and GSI graphics. TXT is a lightweight text representation of the calculated breakdowns and support recommendation.

## Methods implemented

### RMR

The implementation uses the following components:

| Parameter                | Input     | Implemented contribution |
| ------------------------ | --------- | -----------------------: |
| Intact rock strength     | UCS (MPa) |                     0–15 |
| Rock Quality Designation | RQD (%)   |                     3–20 |
| Joint spacing            | m         |                     5–20 |
| Joint condition          | category  |                     0–30 |
| Groundwater              | category  |                     0–15 |
| Orientation adjustment   | category  |                -12 to +5 |

The exact category thresholds and mappings are documented in [`docs/engineering.md`](docs/engineering.md).

### Q-System

The calculation uses:

`Q = (RQD / Jn) × (Jr / Ja) × (Jw / SRF)`

The implementation clamps `Jn`, `Ja`, and `SRF` to a minimum of `0.1` before division. It does not otherwise validate the physical range or category validity of Q-System inputs.

### GSI

The implementation starts with a structure-dependent base value and applies a surface-condition adjustment. The structure values are represented as midpoints of broad ranges in the source code.

The GUI also collects a `weathering` string, but that field is currently retained only in the result breakdown and does not alter the computed GSI.

### Support recommendation

The current support module maps Q to six broad categories and assigns bolt spacing, shotcrete thickness, and an empirical bolt-length estimate.

This is deliberately documented as **simplified software logic**, not as a complete implementation of the NGI support-design methodology. See [`docs/engineering.md`](docs/engineering.md).

## Application workflow

1. Install the Python dependencies.
2. Start the application with `python -m gui.app`.
3. Enter the RMR, Q-System, and GSI parameters.
4. Select **Run Classification**.
5. Review RMR, Q, GSI, and the support category.
6. Review the RMR chart in the GUI.
7. Export a PDF, DOCX, or TXT report if required.

The GUI currently shows the RMR chart after a calculation. The Q-System and GSI charts are generated for reports but are not currently displayed in the live GUI plot panel.

## Requirements

The repository currently pins its Python dependencies in `requirements.txt`, including:

- Python packages for PySide6
- Matplotlib and NumPy
- ReportLab
- python-docx
- supporting packages

The project does not currently provide a repository-level `pyproject.toml` despite the original README describing one, so `requirements.txt` is the authoritative dependency list in the current tree.

## Installation

Create and activate a virtual environment from the repository root.

### Windows

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / macOS

```text
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then start the application:

```text
python -m gui.app
```

See [`docs/installation.md`](docs/installation.md) for troubleshooting and environment notes.

## Running the application

From the repository root:

```text
python -m gui.app
```

The main window contains:

- **Input panel** on the left.
- **Results panel** on the upper-right.
- **Plot panel** on the lower-right.
- **File**, **Export**, and **Help** menus.

The application creates a `reports/` directory in the current working directory when the main window module is loaded.

## Using the GUI

The input panel currently consists of free-text `QLineEdit` fields. There are no combo boxes, range validators, or schema-level GUI validators.

For reliable operation, use the exact category strings expected by the calculation modules.

### RMR categories

Joint condition:

```text
very_rough
rough
slightly_rough
smooth
slickensided
soft_infill
very_soft_infill
```

Groundwater:

```text
dry
damp
wet
dripping
flowing
```

Orientation:

```text
very_favorable
favorable
fair
unfavorable
very_unfavorable
```

### GSI categories

Structure:

```text
massive
blocky
very_blocky
disintegrated
laminated
sheared
```

Surface condition:

```text
fresh
slightly_weathered
moderately_weathered
highly_weathered
```

The weathering field is currently stored but does not affect the numerical GSI calculation.

## Outputs and reports

After a successful calculation, the application stores the result in a `ClassificationResult` object.

### PDF

The PDF contains:

- RMR, Q-System, and GSI summary values.
- Support recommendation data.
- RMR breakdown table.
- Q-System breakdown table.
- GSI breakdown table.
- RMR chart.
- Q-System chart.
- GSI diagram.

### DOCX

The DOCX contains the same main numerical breakdowns and charts, with the charts placed on separate pages.

### TXT

The TXT report contains:

- RMR breakdown.
- Q-System breakdown.
- GSI breakdown.
- Support recommendation fields.

The GUI currently writes fixed filenames to a `reports/` directory:

```text
reports/rockmass_report.pdf
reports/rockmass_report.docx
reports/rockmass_report.txt
```

Chart PNG files are also created in that directory during PDF/DOCX generation.

## Project structure

```text
rockmass-classification-tool/
├── docs/
│   ├── architecture.md
│   ├── changelog.md
│   ├── engineering.md
│   ├── installation.md
│   ├── troubleshooting.md
│   └── usage.md
├── examples/
├── gui/
│   ├── app.py
│   ├── main_window.py
│   └── widgets/
│       ├── input_panel.py
│       ├── plot_panel.py
│       └── result_panel.py
├── src/
│   └── rockmass/
│       ├── models.py
│       ├── rmr.py
│       ├── qsystem.py
│       ├── gsi.py
│       ├── support.py
│       ├── plotting.py
│       └── reports/
│           ├── report_pdf.py
│           ├── report_docx.py
│           └── report_txt.py
├── tests/
│   ├── test_gsi.py
│   ├── test_qsystem.py
│   ├── test_rmr.py
│   └── test_support.py
├── LICENSE
├── README.md
└── requirements.txt
```

## Python API

The calculation modules can be used independently of the GUI.

### RMR

```python
from src.rockmass.models import RMRInput
from src.rockmass.rmr import compute_rmr

data = RMRInput(
    ucs=100,
    rqd=80,
    joint_spacing=0.5,
    joint_condition="rough",
    groundwater="damp",
    orientation="fair",
)

value, breakdown = compute_rmr(data)
```

### Q-System

```python
from src.rockmass.models import QSystemInput
from src.rockmass.qsystem import compute_q

data = QSystemInput(
    rqd=80,
    jn=9,
    jr=2,
    ja=2,
    jw=1,
    srf=1,
)

value, breakdown = compute_q(data)
```

### GSI

```python
from src.rockmass.models import GSIInput
from src.rockmass.gsi import compute_gsi

data = GSIInput(
    structure="blocky",
    surface_condition="slightly_weathered",
    weathering="moderate",
)

value, breakdown = compute_gsi(data)
```

### Support

```python
from src.rockmass.support import compute_support

support = compute_support(q_value=10, span=5)
```

## Testing

The repository contains four test files corresponding to the main engineering modules:

- `test_rmr.py`
- `test_qsystem.py`
- `test_gsi.py`
- `test_support.py`

At the current repository state, these files are placeholders rather than populated automated test suites. Therefore the existence of the test directory should not be interpreted as evidence that the engineering calculations are comprehensively regression-tested.

A future test suite should cover:

- Every rating threshold, including exact boundary values.
- Valid and invalid categorical inputs.
- Zero and negative numeric inputs.
- Q-System denominator handling.
- GSI structure and surface-condition combinations.
- Support threshold boundaries.
- Report generation.
- GUI-to-backend integration.

## Documentation

| Document                                             | Purpose                                                                   |
| ---------------------------------------------------- | ------------------------------------------------------------------------- |
| [`docs/installation.md`](docs/installation.md)       | Environment setup, dependency installation, and launch instructions       |
| [`docs/usage.md`](docs/usage.md)                     | End-user workflow and input guidance                                      |
| [`docs/engineering.md`](docs/engineering.md)         | Implemented equations, mappings, assumptions, and engineering limitations |
| [`docs/architecture.md`](docs/architecture.md)       | Software architecture and data flow                                       |
| [`docs/troubleshooting.md`](docs/troubleshooting.md) | Common runtime and input problems                                         |
| [`docs/changelog.md`](docs/changelog.md)             | Documentation of project changes and release notes                        |

## Engineering scope and limitations

The software should be regarded as a classification and reporting aid rather than a complete geotechnical design system.

Important current implementation limitations include:

1. **Input validation is minimal.** GUI fields are free text and numeric conversion errors can terminate the classification action rather than presenting a structured validation message.
2. **Unknown categorical values silently fall back to defaults** in several calculation functions.
3. **RMR class labels are not calculated.** The software returns a numerical RMR value and component breakdown but does not currently assign the conventional RMR rock-mass class in the backend.
4. **GSI is simplified.** The implementation uses lookup midpoints plus a surface adjustment rather than a full graphical/observational GSI assessment workflow.
5. **Weathering is not part of the current GSI calculation.**
6. **Support logic is simplified.** The Q-based support table is not a full implementation of excavation-support design charts or project-specific support design.
7. **No excavation span is collected by the GUI.** The support function uses its default span of 5 m when called from the GUI.
8. **The live GUI displays only the RMR chart.** Q and GSI graphics are generated during report creation.
9. **Reports overwrite fixed filenames** when exported repeatedly in the same working directory.
10. **Automated tests are currently empty placeholders.**
11. **The repository currently has no `pyproject.toml`**, although the original README refers to one.

These points are intentionally explicit so that the documentation reflects the current implementation rather than overstating the software's engineering scope.

## Development

The core architecture intentionally keeps engineering calculations separate from GUI code. New calculation methods should follow the same pattern:

1. Define a typed/dataclass input model.
2. Implement a pure calculation function.
3. Return both the final value and a transparent breakdown.
4. Add tests for normal and boundary cases.
5. Integrate the result into `ClassificationResult`.
6. Add GUI presentation only after the backend behavior is stable.
7. Update the relevant documentation.

See [`docs/architecture.md`](docs/architecture.md) for the current dependency and data-flow model.

## License

This project is distributed under the MIT License. See [`LICENSE`](LICENSE).
