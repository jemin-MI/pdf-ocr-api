import fitz  # PyMuPDF for extracting text from PDFs
import os
from datetime import datetime


def get_text_from_file(file):
    """Extract text from a PDF file using PyMuPDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")  # Read from file stream
    text = "\n".join([page.get_text() for page in doc])  # Extract text from all pages
    return text.strip() if text else "No text found in PDF."

def save_text_file(dir_location, content):
    os.makedirs(dir_location, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    summary_file_name = f"{dir_location}/summarised_text_{timestamp}.txt"

    with open(summary_file_name, "w") as file:
        file.write(str(content))
