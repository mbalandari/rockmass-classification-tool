# Installation and Environment Setup

## 1. Prerequisites

The application is a Python desktop application built with PySide6.

The current dependency set is pinned in `requirements.txt`. It includes:

- PySide6
- Matplotlib
- NumPy
- ReportLab
- python-docx
- supporting plotting, document, and runtime packages

## 2. Clone the repository

From a terminal:

```text
git clone https://github.com/mbalandari/rockmass-classification-tool.git
cd rockmass-classification-tool
```

## 3. Create a virtual environment

### Windows

```text
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```text
python3 -m venv .venv
source .venv/bin/activate
```

Using a virtual environment is strongly recommended because the project pins a complete dependency set.

## 4. Install dependencies

```text
pip install -r requirements.txt
```

If `pip` is associated with a different Python installation, use:

```text
python -m pip install -r requirements.txt
```

or, on systems where Python 3 is invoked as `python3`:

```text
python3 -m pip install -r requirements.txt
```

## 5. Launch the application

Run from the repository root:

```text
python -m gui.app
```

The application creates the Qt application object, constructs the main window, displays it, and enters the Qt event loop.

## 6. Working directory

The GUI creates a directory named `reports` relative to the **current working directory** when `gui.main_window` is imported.

For predictable output locations, start the program from the repository root:

```text
cd rockmass-classification-tool
python -m gui.app
```

## 7. Report dependencies

PDF export requires ReportLab.

DOCX export requires python-docx.

Matplotlib and its Qt backend are required for chart generation and GUI plotting.

## 8. Verifying the installation

A minimal verification is to launch the GUI and confirm that:

1. The main window opens.
2. The input panel is visible.
3. The results panel is visible.
4. The plot panel is visible.
5. Clicking **Run Classification** with valid values produces a result.
6. Exporting a report creates the expected file in `reports/`.

## 9. Recommended development setup

For development:

```text
python -m venv .venv
# activate .venv
python -m pip install -r requirements.txt
python -m gui.app
```

Keep the virtual environment outside version control; `.gitignore` should exclude it.

## 10. Troubleshooting installation

If imports fail, first confirm that:

- the virtual environment is active,
- dependencies were installed into that same environment,
- the command is being executed from the repository root,
- and the Python interpreter being used is the expected one.

For runtime-specific problems, see [`troubleshooting.md`](troubleshooting.md).
