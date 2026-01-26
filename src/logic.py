from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path, start_page, end_page, output_path):
    """
    Splits a PDF file extracting pages from start_page to end_page (inclusive).

    Args:
        input_path (str): The path to the source PDF file.
        start_page (int): The first page to include (1-based index).
        end_page (int): The last page to include (1-based index).
        output_path (str): The path where the split PDF will be saved.

    Returns:
        tuple: A tuple containing the output path and the total number of pages in the original PDF.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If the page range is invalid.
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    reader = PdfReader(input_path)
    num_pages = len(reader.pages)

    if start_page < 1 or end_page > num_pages or start_page > end_page:
        raise ValueError("Invalid page range.")

    writer = PdfWriter()
    
    # Subtract 1 because PdfReader uses 0-based indexing, but input is 1-based
    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path, num_pages
