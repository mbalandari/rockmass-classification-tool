# Rock Mass Classification Tool

A desktop application for rock mass classification using:

- **RMR (Rock Mass Rating, Bieniawski)**
- **Q-System (Barton et al.)**
- **GSI (Geological Strength Index, Hoek & Marinos)**

Built with **PySide6**, this tool provides a clean GUI, engineering‑grade charts, and exportable reports for practical geotechnical and rock mechanics work.

---

## ✨ Features

### Rock Mass Classification

- Compute **RMR** with full parameter breakdown.
- Compute **Q-System** with full parameter breakdown.
- Compute **GSI** based on structure and surface condition.
- Generate **support recommendations** based on Q-System.

### Engineering Charts

- **RMR bar chart** with professional styling.
- **Q-System radar chart**.
- **GSI diagram** with structure domains.

### Reporting

Export reports including:

- Summary values (RMR, Q, GSI).
- Breakdown tables.
- Charts (RMR, Q, GSI).
- Support recommendations.

(Currently PDF/DOCX/TXT generation is implemented in the `reports` module.)

### GUI (PySide6)

- **Input panel** for RMR, Q-System, and GSI parameters.
- **Results panel** showing computed values and support recommendations.
- **Plot panel** for charts.
- Menu bar with:
  - **File** → Exit
  - **Export** → PDF, DOCX, TXT
  - **Help** → About dialog.

---

## 📁 Project Structure

```text
rockmass-classification-tool/
  gui/
    app.py
    main_window.py
    widgets/
      input_panel.py
      result_panel.py
      plot_panel.py
  src/
    rockmass/
      models.py
      rmr.py
      qsystem.py
      gsi.py
      support.py
      plotting.py
      reports/
        report_pdf.py
        report_docx.py
        report_txt.py
  docs/
  tests/
  pyproject.toml
  README.md
```

- gui/ — Application entry point and GUI components.
- src/rockmass/ — Core calculation logic (RMR, Q-System, GSI, support).
- src/rockmass/plotting.py — Chart and diagram generation.
- src/rockmass/reports/ — Report generation (PDF, DOCX, TXT).
- docs/ — Documentation (usage, methods, internals).
- tests/ — Test scaffolding.
- pyproject.toml — Project configuration.

---

## 🚀 Installation & Running

### 1. Install dependencies

From the project root:

```bash
pip install -r requirements.txt
```

(or, if you use pipx / virtualenv, activate your environment first.)

### 2. Run the application

From the project root:

```bash
python -m gui.app
```

This will launch the main window with:

- Left: Input panel.
- Right top: Results panel.
- Right bottom: Plot panel.

---

## 🧱 Inputs Overview (Short)

A detailed guide is in the docs, but briefly:

- RMR inputs (via InputPanel):
  - UCS (MPa)
  - RQD (%)
  - Joint spacing (m)
  - Joint condition
  - Groundwater condition
  - Orientation

- Q-System inputs:
  - RQD
  - Jn (joint set number)
  - Jr (joint roughness)
  - Ja (joint alteration)
  - Jw (water reduction factor)
  - SRF (stress reduction factor)

- GSI inputs:
  - Structure
  - Surface condition
  - Weathering

For a full explanation of each input, allowed values, and how to avoid errors, see:

- docs/gui_usage.md
- docs/rmr.md
- docs/qsystem.md
- docs/gsi.md

---

## 📤 Exporting Reports

Use the Export options in the menu bar:

- Export PDF → generates a PDF report.
- Export DOCX → generates a Word report.
- Export TXT → generates a text summary.
- Reports are written to the reports directory (see src/rockmass/reports/ for implementation details).

---

## 📄 Documentation

Detailed documentation is provided in the docs/ folder:

- docs/gui_usage.md — How to use the app, input details, and error‑free usage.
- docs/rmr.md — RMR methodology and implementation notes.
- docs/qsystem.md — Q-System formula, parameters, and usage.
- docs/gsi.md — GSI concept, structure domains, and diagram.
- docs/support.md — Support recommendation logic.
- docs/reports.md — Report contents and structure.
- docs/packaging.md — Optional notes on packaging the app.

---

## 🧪 Tests

The tests/ folder is prepared for:

- RMR calculation tests.
- Q-System tests.
- GSI tests.
- Support module tests.
- Plotting tests.
- Tests can be expanded to validate engineering logic and ensure stability.

---

## 👤 Author

Developed by M. Balandari Toroghi  
Rock mechanics specialist & software developer.

---
