import tkinter as tk
from .interface import PDFSplitterApp

try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

def main():
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
