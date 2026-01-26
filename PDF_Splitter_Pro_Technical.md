# PDF Splitter Pro - Technical Documentation

This document provides a technical overview of the PDF Splitter Pro application for developers.

## Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core programming language |
| **Tkinter** | GUI framework (built-in) |
| **tkinterdnd2** | Drag & Drop support for Tkinter |
| **PyPDF2** | PDF manipulation library |
| **Pillow** | Image processing for icons |
| **PyInstaller** | Packaging into standalone executable |
| **Black** | Code formatting |

## Project Structure

```
PDFsplitter/
├── src/                    # Source code
│   ├── main.py             # Application entry point
│   ├── interface.py        # GUI implementation (PDFSplitterApp class)
│   └── logic.py            # PDF splitting logic (split_pdf function)
├── assets/                 # Static resources
│   └── icon.png            # Application icon
├── build.py                # Build automation script
├── PDFsplitter_main.spec   # PyInstaller configuration
├── requirements.txt        # Python dependencies
├── README.md               # User documentation
└── TECHNICAL.md            # This file
```

## Architecture Overview

```
┌────────────────────────────────────┐
│            main.py                 │
│         (Entry Point)              │
└────────────────┬───────────────────┘
                 │
                 ▼
┌────────────────────────────────────┐
│       PDFSplitterApp               │
│       (interface.py)               │
│                                    │
│  ┌─────────┐ ┌─────────┐ ┌──────┐  │
│  │DropZone │ │ Inputs  │ │Split │  │
│  └────┬────┘ └─────────┘ └──┬───┘  │
└───────┼─────────────────────┼──────┘
        │                     │
        ▼                     ▼
┌────────────────────────────────────┐
│           logic.py                 │
│         split_pdf()                │
│                                    │
│  PdfReader → Extract → PdfWriter   │
└────────────────────────────────────┘
```

## Module Descriptions

### `src/main.py`
Entry point of the application. Initializes the Tkinter root window with optional Drag & Drop support if `tkinterdnd2` is available.

```python
def main():
    """
    Main entry point of the application.
    """
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
```

### `src/interface.py`
Contains the `PDFSplitterApp` class which handles:
- GUI layout and styling
- Event bindings (click, hover, drag & drop)
- User interactions (file selection, page range input)
- Visual feedback (success/error states)

```python
class PDFSplitterApp:
    """
    Main application class for PDF Splitter Pro.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter Pro")
        self.root.geometry("520x420")
        self.pdf_path = None
        # ... GUI setup ...
```

### `src/logic.py`
Contains the `split_pdf` function which:
- Reads the source PDF using `PyPDF2.PdfReader`
- Extracts specified page range (1-based indexing)
- Writes output using `PyPDF2.PdfWriter`

```python
def split_pdf(input_path, start_page, end_page, output_path):
    """
    Splits a PDF file extracting pages from start_page to end_page.
    """
    reader = PdfReader(input_path)
    num_pages = len(reader.pages)
    
    writer = PdfWriter()
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    return output_path, num_pages
```

## Data Flow

```
User
  │
  │ 1. Drag & Drop PDF
  ▼
interface.py ──2. Validate──▶ logic.py
  │                             │
  │ 3. Show page count          │ PyPDF2
  ▼                             ▼
UI Updated                  PdfReader
  │
  │ 4. Click Split
  ▼
interface.py ──5. Split──▶ logic.py
                              │
                              ▼
                         Output PDF
```

## Build Process

```
    build.py
        │
   ┌────┴────┐
   ▼         ▼
clean()   build()
   │         │
   │         ▼
   │    PyInstaller
   │         │
   ▼         ▼
Remove    PDF Splitter
dist/     Pro.exe
build/
```

## Key Design Decisions

1. **Relative Imports**: The `src/` package uses relative imports (e.g., `from .logic import split_pdf`) to maintain clean module separation.

2. **Dual Icon Loading**: The interface loads icons differently based on whether the app is frozen (packaged) or running from source, using `sys._MEIPASS` for packaged assets.

3. **Graceful Degradation**: If `tkinterdnd2` is unavailable, the app falls back to standard Tkinter without drag & drop.

4. **Environment Isolation**: The build script uses `sys.executable` to ensure PyInstaller runs in the correct virtual environment.

## Running the Application

```bash
# From source
python -m src.main

# Build executable
python build.py

# Run executable
./dist/PDF\ Splitter\ Pro.exe
```

