# Troubleshooting

## Application does not start

### Check the working directory

Run the command from the repository root:

```text
python -m gui.app
```

### Check the virtual environment

Confirm the environment is active and dependencies were installed into it:

```text
python -m pip install -r requirements.txt
```

### Check PySide6

If the import fails, verify:

```text
python -c "import PySide6; print(PySide6.__version__)"
```

## `ModuleNotFoundError`

The application imports backend modules using paths such as:

```text
from src.rockmass.models import ...
```

Start the application from the repository root so that the project root is on Python's import path.

If the error concerns a third-party library, reinstall the pinned requirements:

```text
python -m pip install -r requirements.txt
```

## The application crashes when Run Classification is clicked

The current GUI converts text directly with `float(...)`.

For example:

```text
float("abc")
```

raises a conversion error.

Make sure numeric fields contain valid numeric values.

At present, the GUI does not provide a dedicated validation dialog for malformed numeric input.

## Results look unexpected

### Check categorical spelling

The backend expects exact lowercase strings such as:

```text
rough
damp
fair
blocky
slightly_weathered
```

For categorical fields, using a different spelling can cause a default mapping to be used.

### Check boundary values

The RMR rating functions use strict `>` comparisons.

For example, UCS exactly equal to 100 MPa is not placed in the `>100` band; it falls into the next branch.

The same principle applies to RQD, joint spacing, and support thresholds.

See [`engineering.md`](engineering.md) for the exact implementation tables.

## GSI does not change when weathering changes

This is expected with the current implementation.

The `weathering` field is stored in `GSIInput` and returned in the breakdown, but `compute_gsi()` does not use it in the numerical calculation.

GSI currently depends on:

```text
structure
surface_condition
```

## Q calculation behaves strangely for zero values

The Q implementation prevents division by zero by replacing `Jn`, `Ja`, and `SRF` values below `0.1` with `0.1`.

This is a numerical safeguard, not a substitute for valid engineering input selection.

## Support recommendation uses an unexpected bolt length

The support module calculates:

```text
bolt_length = 2.0 + 0.15 × span
```

The GUI does not ask for span and calls `compute_support(q_value)` without an explicit span.

The default span is therefore 5.0 m, producing a 2.75 m calculated bolt length.

## The Q or GSI chart is not visible in the GUI

This is currently expected.

After classification, the live GUI plot panel is updated with the RMR bar chart.

The Q radar chart and GSI diagram are generated during PDF/DOCX report creation but are not currently displayed in the live plot panel.

## Export does nothing or shows "No Result"

Reports can only be exported after a classification has been successfully run.

Click:

```text
Run Classification
```

first.

## Reports cannot be found

The application creates the report directory relative to the process's current working directory.

Start the application from the repository root and check:

```text
reports/
```

Expected filenames are:

```text
rockmass_report.pdf
rockmass_report.docx
rockmass_report.txt
```

## Previous reports disappeared

The GUI uses fixed filenames, so subsequent exports overwrite the previous report of the same format.

Copy or rename reports externally if you need to preserve multiple calculation cases.

## PDF/DOCX export fails

Check that the corresponding dependencies are installed:

```text
python -m pip install -r requirements.txt
```

PDF generation requires ReportLab.

DOCX generation requires python-docx.

## Report charts remain in the report directory

PDF and DOCX generation creates:

```text
rmr_chart.png
q_chart.png
gsi_chart.png
```

These are intermediate files used to assemble the report.

## Tests appear to do nothing

The repository contains test filenames, but the current test files are empty placeholders.

Do not interpret their presence as evidence of a completed automated test suite.

## Need to determine whether a behavior is intentional

Use the source implementation as the authoritative description of current behavior:

- RMR → `src/rockmass/rmr.py`
- Q-System → `src/rockmass/qsystem.py`
- GSI → `src/rockmass/gsi.py`
- Support → `src/rockmass/support.py`
- GUI orchestration → `gui/main_window.py`
- Reports → `src/rockmass/reports/`

If documentation and source disagree, the source should be treated as the current implementation until the code is changed.
