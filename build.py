import os
import shutil
import subprocess
import sys

def clean_build():
    """Remove dist and build directories."""
    dirs_to_remove = ['dist', 'build']
    for d in dirs_to_remove:
        if os.path.exists(d):
            print(f"Removing {d}...")
            shutil.rmtree(d)

def build():
    """Run PyInstaller."""
    print("Starting build process...")
    # Use sys.executable to ensure we use the same environment (venv)
    subprocess.run([sys.executable, '-m', 'PyInstaller', 'PDFsplitter_main.spec'], check=True)
    print("Build complete.")

if __name__ == "__main__":
    clean_build()
    build()
