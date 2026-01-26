import tkinter as tk
try:
    from .interface import PDFSplitterApp
except ImportError:
    from src.interface import PDFSplitterApp


try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

def main():
    """
    Main entry point of the application.
    Initializes the Tkinter root window (with Drag & Drop support if available)
    and launches the PDFSplitterApp.
    """
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
