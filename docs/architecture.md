# Software Architecture

## Overview

The application uses a small layered architecture:

```text
┌─────────────────────────────┐
│        PySide6 GUI          │
│  app / main window / UI     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Domain models         │
│ RMRInput / QSystemInput /   │
│ GSIInput / Classification   │
│ Result                      │
└──────────────┬──────────────┘
               │
       ┌───────┼────────┬──────────┐
       ▼       ▼        ▼          ▼
     RMR      Q-System  GSI      Support
       │       │        │          │
       └───────┴────────┴──────────┘
               │
               ▼
        ClassificationResult
               │
       ┌───────┴───────────┐
       ▼                   ▼
   Plotting             Reports
                        PDF/DOCX/TXT
```

The important design principle is that the engineering calculations live outside the GUI.

## Repository layers

### `gui/`

Contains the PySide6 application shell and widgets.

- `gui/app.py` — application entry point.
- `gui/main_window.py` — window composition, classification orchestration, menu actions, and export actions.
- `gui/widgets/input_panel.py` — user input fields.
- `gui/widgets/result_panel.py` — headline result display.
- `gui/widgets/plot_panel.py` — Matplotlib-backed live plot display.

### `src/rockmass/`

Contains the core domain logic.

- `models.py` — dataclasses used to pass classification inputs and results.
- `rmr.py` — RMR ratings and calculation.
- `qsystem.py` — Q-System calculation.
- `gsi.py` — GSI lookup and adjustment.
- `support.py` — simplified support recommendation.
- `plotting.py` — engineering visualizations.

### `src/rockmass/reports/`

Contains report generators:

- `report_pdf.py`
- `report_docx.py`
- `report_txt.py`

Each generator consumes a `ClassificationResult` and produces a report artifact.

## Main data flow

### 1. User input

`InputPanel` exposes `QLineEdit` controls.

The GUI does not create typed domain objects until the user clicks **Run Classification**.

### 2. Input model creation

`MainWindow.run_classification()` converts numeric text to floats and creates:

- `RMRInput`
- `QSystemInput`
- `GSIInput`

### 3. Calculation

The three classification functions are called:

```text
compute_rmr()
compute_q()
compute_gsi()
```

The resulting Q value is passed to:

```text
compute_support()
```

### 4. Result aggregation

The values are combined into:

```text
ClassificationResult
```

This object stores:

- RMR
- RMR breakdown
- Q
- Q breakdown
- GSI
- GSI breakdown
- support recommendations

### 5. GUI update

The result object is stored as `last_result`.

The Results panel displays the headline values and support category.

The plot panel is updated with a newly generated RMR bar chart.

### 6. Report generation

When the user selects a report format, the corresponding report class receives `last_result`.

PDF and DOCX generation also call the plotting functions to create PNG assets.

## Dependency direction

The intended dependency direction is:

```text
GUI → domain models/calculations → result
GUI → report generators
Reports → plotting
```

The core calculation modules do not depend on PySide6.

This makes the calculation functions suitable for unit testing and programmatic use without launching the GUI.
