# User Guide

## 1. Start the application

From the repository root:

```text
python -m gui.app
```

The application opens a desktop window titled **Rock Mass Classification Tool**.

The main window is divided into:

- **Input Parameters** — left side.
- **Results** — upper-right.
- **Plot** — lower-right.

The application also provides **File**, **Export**, and **Help** menus.

## 2. Enter input data

The input panel contains free-text fields for all three classification systems.

### RMR inputs

| Field             | Expected value                           |
| ----------------- | ---------------------------------------- |
| UCS (MPa)         | Numeric uniaxial compressive strength    |
| RQD (%)           | Numeric RQD percentage                   |
| Joint Spacing (m) | Numeric average joint spacing            |
| Joint Condition   | One of the supported category strings    |
| Groundwater       | One of the supported category strings    |
| Orientation       | One of the supported orientation strings |

### Q-System inputs

| Field | Expected value                  |
| ----- | ------------------------------- |
| RQD   | Numeric RQD value               |
| Jn    | Numeric joint-set number        |
| Jr    | Numeric joint roughness number  |
| Ja    | Numeric joint alteration number |
| Jw    | Numeric water reduction factor  |
| SRF   | Numeric stress reduction factor |

The RQD entered here is independent of the RMR RQD field at the UI level, although both fields are currently backed by the same `QLineEdit` in the GUI and therefore share the same entered value.

### GSI inputs

| Field             | Expected value                           |
| ----------------- | ---------------------------------------- |
| Structure         | Supported structure category             |
| Surface Condition | Supported surface-condition category     |
| Weathering        | Free text stored in the result breakdown |

The current GSI implementation does not use the weathering field to calculate the numerical GSI.

## 3. Supported category strings

### Joint condition

```text
very_rough
rough
slightly_rough
smooth
slickensided
soft_infill
very_soft_infill
```

### Groundwater

```text
dry
damp
wet
dripping
flowing
```

### Orientation

```text
very_favorable
favorable
fair
unfavorable
very_unfavorable
```

### GSI structure

```text
massive
blocky
very_blocky
disintegrated
laminated
sheared
```

### GSI surface condition

```text
fresh
slightly_weathered
moderately_weathered
highly_weathered
```

Use lowercase strings exactly as shown. The current GUI does not provide dropdown selectors or automatic normalization.

## 4. Run classification

Click **Run Classification**.

The application:

1. Converts the numeric text fields to floating-point values.
2. Builds `RMRInput`, `QSystemInput`, and `GSIInput` objects.
3. Calculates RMR.
4. Calculates Q.
5. Calculates GSI.
6. Calculates the simplified Q-based support recommendation.
7. Combines the results in `ClassificationResult`.
8. Updates the Results panel.
9. Generates and displays the RMR bar chart.
10. Stores the result for later report export.

A success dialog is then shown.

## 5. Read the results

The Results panel shows:

- RMR
- Q-System value
- GSI
- Support category

The current result panel intentionally displays headline values only. Detailed component breakdowns are available in the generated reports and through the backend result object.

## 6. Understand the RMR chart

The live GUI chart is the RMR contribution bar chart.

Each bar represents one contribution:

- strength
- RQD
- joint spacing
- joint condition
- groundwater
- orientation

The orientation contribution can be negative, so the chart can contain a bar below zero.

## 7. Export reports

Use the **Export** menu.

### Export PDF

Select:

```text
Export → Export PDF
```

The application writes:

```text
reports/rockmass_report.pdf
```

### Export DOCX

Select:

```text
Export → Export DOCX
```

The application writes:

```text
reports/rockmass_report.docx
```

### Export TXT

Select:

```text
Export → Export TXT
```

The application writes:

```text
reports/rockmass_report.txt
```

Export is disabled logically until a classification result exists. If no result has been calculated, the application displays a warning.

## 8. Generated report graphics

PDF and DOCX generation creates three PNG files in the same report directory:

```text
rmr_chart.png
q_chart.png
gsi_chart.png
```

These are intermediate report assets and may be overwritten by a subsequent export.

## 9. Important input behavior

The current GUI performs limited validation.

For example, numeric fields are converted with `float(...)`. Non-numeric input can therefore produce a Python conversion exception rather than a friendly field-level validation message.

Unknown categorical values are not rejected consistently. Several backend mappings use a default rating when the supplied key is not recognized.

For reliable use, enter values and category strings exactly as documented.

## 10. Span and support recommendations

The support calculation accepts an excavation span and uses it to estimate bolt length:

```text
bolt_length = 2.0 + 0.15 × span
```

However, the current GUI does not provide a span field. When the GUI calculates support, it calls the function without a span and therefore uses the backend default of **5.0 m**.

The resulting support recommendation should therefore be interpreted as a simplified software output rather than a project-specific support design.

## 11. Programmatic use

The calculation modules can also be called without launching the GUI.

See the API examples in the root [`README.md`](../README.md) and the engineering details in [`engineering.md`](engineering.md).
