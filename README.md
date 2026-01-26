# PDF Splitter Pro

A professional tool to split PDF documents with a modern and elegant user interface.

## Features

- **Drag & Drop Interface**: Easily load files by dragging them into the application.
- **Visual Feedback**: Interactive UI with hover effects and status indicators.
- **Custom Split Ranges**: Define start and end pages to extract specific sections.
- **Portable**: Available as a standalone Windows executable.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/PDFsplitter.git
   cd PDFsplitter
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application with Python:
```bash
python PDFsplitter_main.py
```

## Build Executable

To generate a standalone `.exe` version:

```bash
python build.py
```

The executable will be created in the `dist/` folder with the name `PDF Splitter Pro.exe`.
