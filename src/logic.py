from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path, start_page, end_page, output_path):
    """
    Divide un PDF desde la página start_page hasta end_page (inclusive).
    Las páginas comienzan en 1.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")
    reader = PdfReader(input_path)
    num_pages = len(reader.pages)
    if start_page < 1 or end_page > num_pages or start_page > end_page:
        raise ValueError("Rango de páginas inválido.")
    writer = PdfWriter()
    for i in range(start_page-1, end_page):
        writer.add_page(reader.pages[i])
    with open(output_path, 'wb') as f:
        writer.write(f)
    return output_path, num_pages
