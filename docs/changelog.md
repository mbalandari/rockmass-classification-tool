# Changelog

This changelog documents all notable changes to the Rock Mass Classification Tool.  
Version numbers follow semantic versioning: MAJOR.MINOR.PATCH.

---

## v1.0.0 — Initial Release

### Added

- Complete GUI built with PySide6:
  - Main window
  - Input panel (RMR, Q-System, GSI)
  - Results panel
  - Plot panel (RMR chart)
- Core rock mass classification modules:
  - RMR computation
  - Q-System computation
  - GSI computation
  - Support recommendation engine
- Plotting module for:
  - RMR bar chart
  - Q-System radar chart (for reports)
  - GSI diagram (for reports)
- Report generation system:
  - PDF export
  - DOCX export
  - TXT export
- Documentation structure (`docs/` folder)
- Project README
- Basic test scaffolding
- Clean project layout using `gui/` and `src/rockmass/` architecture

### Notes

This version establishes the foundation of the application.  
All core features are implemented and functional.

---

## Planned for v1.1.0

### To be added

- Automatic elastic region detection (for future UCS integration)
- Multi-specimen batch processing
- JSON export option
- Additional plot customization
- Improved error dialogs
- Optional smoothing filters for charts

### To be improved

- GUI layout responsiveness
- Report formatting consistency
- Input validation messages

---

## Planned for v2.0.0 (Major Update)

### Major features

- Multi-specimen comparison dashboard
- Statistical summaries (mean, std, min, max)
- Export full analysis session as a project file
- Packaging into downloadable executables (Windows/macOS/Linux)
- Advanced support design module (bolt patterns, shotcrete design curves)

---
