# Engineering Methods and Implementation Notes

## Purpose

This document describes the engineering calculations **as implemented in the current source code**.

It deliberately distinguishes software behavior from the broader published methodologies. The application currently provides simplified classification and support logic and should not be interpreted as a complete implementation of every chart, adjustment, or design procedure associated with RMR, Q, or GSI.

## 1. RMR implementation

The backend calculates:

```text
RMR = R1 + R2 + R3 + R4 + R5 + R6
```

where:

- `R1` = intact rock strength rating
- `R2` = RQD rating
- `R3` = joint-spacing rating
- `R4` = joint-condition rating
- `R5` = groundwater rating
- `R6` = orientation adjustment

### 1.1 UCS rating

Input: UCS in MPa.

| Condition in implementation | Rating |
| --------------------------- | -----: |
| UCS > 250                   |     15 |
| 100 < UCS ≤ 250             |     12 |
| 50 < UCS ≤ 100              |      7 |
| 25 < UCS ≤ 50               |      4 |
| 5 < UCS ≤ 25                |      2 |
| UCS ≤ 5                     |      0 |

The use of strict `>` comparisons is important: exact boundary values fall into the lower rating band.

### 1.2 RQD rating

Input: RQD in percent.

| Condition in implementation | Rating |
| --------------------------- | -----: |
| RQD > 90                    |     20 |
| 75 < RQD ≤ 90               |     17 |
| 50 < RQD ≤ 75               |     13 |
| 25 < RQD ≤ 50               |      8 |
| RQD ≤ 25                    |      3 |

The current implementation does not explicitly clamp RQD to 0–100.

### 1.3 Joint-spacing rating

Input: average joint spacing in metres.

| Condition in implementation | Rating |
| --------------------------- | -----: |
| spacing > 2.0 m             |     20 |
| 0.6 < spacing ≤ 2.0 m       |     15 |
| 0.2 < spacing ≤ 0.6 m       |     10 |
| 0.06 < spacing ≤ 0.2 m      |      8 |
| spacing ≤ 0.06 m            |      5 |

### 1.4 Joint-condition rating

The current categorical mapping is:

| Category           | Rating |
| ------------------ | -----: |
| `very_rough`       |     30 |
| `rough`            |     25 |
| `slightly_rough`   |     25 |
| `smooth`           |     20 |
| `slickensided`     |     10 |
| `soft_infill`      |      5 |
| `very_soft_infill` |      0 |

An unrecognized category returns **10**.

### 1.5 Groundwater rating

| Category   | Rating |
| ---------- | -----: |
| `dry`      |     15 |
| `damp`     |     10 |
| `wet`      |      7 |
| `dripping` |      4 |
| `flowing`  |      0 |

An unrecognized category returns **7**.

### 1.6 Orientation adjustment

| Category           | Adjustment |
| ------------------ | ---------: |
| `very_favorable`   |         +5 |
| `favorable`        |         +2 |
| `fair`             |          0 |
| `unfavorable`      |         -5 |
| `very_unfavorable` |        -12 |

An unrecognized category returns **0**.

### 1.7 RMR implementation caveat

The software returns a numerical RMR and component breakdown but does not currently assign a conventional rock-mass class label in the calculation module.

The orientation value is treated as a direct adjustment, and the software does not expose a separate excavation-type/orientation table.

## 2. Q-System implementation

The source implements:

```text
Q = (RQD / Jn) × (Jr / Ja) × (Jw / SRF)
```

The three multiplicative terms are returned in the breakdown:

```text
RQD_over_Jn
Jr_over_Ja
Jw_over_SRF
```

### 2.1 Denominator protection

Before calculation, the implementation applies:

```text
Jn = max(Jn, 0.1)
Ja = max(Ja, 0.1)
SRF = max(SRF, 0.1)
```

This prevents division by zero.

It is not equivalent to full physical input validation. Negative or otherwise inappropriate values can still produce unexpected results after the minimum clamp.

### 2.2 Q-system validation scope

The current backend does not enforce published category ranges for:

- RQD
- Jn
- Jr
- Ja
- Jw
- SRF

The application therefore assumes that the user has selected technically appropriate values.

## 3. GSI implementation

The implementation uses a simple structure lookup followed by a surface-condition adjustment.

### 3.1 Structure base values

| Structure       | Base value |
| --------------- | ---------: |
| `massive`       |         82 |
| `blocky`        |         70 |
| `very_blocky`   |         60 |
| `disintegrated` |         38 |
| `laminated`     |         30 |
| `sheared`       |         18 |

The source comments identify these as representative midpoints of broad ranges.

An unknown structure returns **50**.

### 3.2 Surface-condition adjustment

| Surface condition      | Adjustment |
| ---------------------- | ---------: |
| `fresh`                |         +5 |
| `slightly_weathered`   |          0 |
| `moderately_weathered` |         -5 |
| `highly_weathered`     |        -10 |

An unknown condition returns **0**.

### 3.3 Weathering field

`GSIInput` contains:

```text
structure
surface_condition
weathering
```

The current `compute_gsi()` function does not use `weathering` in the numerical calculation. It is copied into the returned breakdown.

This is an important implementation detail: entering a different weathering value alone does not change the calculated GSI.

## 4. Support recommendation implementation

The support module maps Q to six simplified categories.

| Q condition | Category            | Bolt spacing | Shotcrete |
| ----------- | ------------------- | -----------: | --------: |
| Q > 40      | No support required |        0.0 m |      0 mm |
| 10 < Q ≤ 40 | Spot bolting        |        2.5 m |      0 mm |
| 4 < Q ≤ 10  | Systematic bolting  |        2.0 m |      0 mm |
| 1 < Q ≤ 4   | Bolting + mesh      |        1.5 m |     50 mm |
| 0.1 < Q ≤ 1 | Shotcrete + bolts   |        1.5 m |     75 mm |
| Q ≤ 0.1     | Heavy support       |        1.0 m |    150 mm |

The boundary values are determined by the source's strict `>` comparisons.

### 4.1 Bolt length

The implementation estimates:

```text
bolt_length = 2.0 + 0.15 × span
```

The default span is 5.0 m, producing a default bolt length of:

```text
2.75 m
```

The GUI does not expose span, so GUI-generated support results use this default.

### 4.2 Engineering limitation

The support function is a compact rule-based approximation. It should not be described as a complete implementation of NGI support design charts, excavation-support interaction, project-specific design, or code-compliant support selection.

Actual support design may require excavation geometry, ESR, span, stress conditions, discontinuity orientation, failure mechanism, groundwater, construction method, reinforcement capacity, load assumptions, and observational/design verification.

## 5. Visualization implementation

### RMR chart

The RMR chart is a bar chart of the component breakdown.

### Q chart

The Q chart is a radar chart generated from the complete Q breakdown dictionary. Note that the breakdown contains both ratio terms and the underlying input values, so the radar chart is a visualization of the returned dictionary rather than a standardized Q-system engineering chart.

### GSI diagram

The GSI graphic divides the vertical scale into broad colored zones and places a marker at the calculated GSI.

The diagram is a software visualization and should not be interpreted as a full reproduction of a published GSI chart.

## 6. Engineering interpretation

The three classifications serve different purposes and should not be treated as interchangeable scores.

- RMR is a multi-parameter rock-mass rating.
- Q is a multiplicative rock-mass classification system that is also commonly associated with tunnel-support assessment.
- GSI is an observational description of rock-mass structure and surface condition used in rock-mass strength characterization.

The software reports them together for comparative characterization. It does not currently provide a formal correlation, reconciliation procedure, Hoek-Brown parameter derivation, or numerical design workflow.

## 7. Recommended professional use

Before using software results in a project deliverable:

1. Verify the source data and representative rock-mass domain.
2. Verify units.
3. Confirm that the selected classification methodology is appropriate to the project.
4. Review each parameter and category assignment.
5. Check boundary values manually.
6. Compare results with field observations and independent calculations.
7. Treat support recommendations as preliminary unless independently verified.
8. Document the methodology version and engineering references used for the project.

## 8. References

The software is described as implementing established rock-mass classification concepts associated with:

- Bieniawski — Rock Mass Rating (RMR).
- Barton, Lien and Lunde — Q-System.
- Hoek and Marinos — Geological Strength Index (GSI).

For project work, users should consult the authoritative editions and project-specific standards rather than relying on this software documentation as the sole engineering reference.
