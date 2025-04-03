import fitz  # PyMuPDF
import re
import json
import nltk
from nltk.tokenize import sent_tokenize



pdf_path = 'Aadhar.pdf'

def get_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    num_pages = pdf_document.page_count
    text = ""
    for page_num in range(num_pages):
        page = pdf_document.load_page(page_num)
        text += page.get_text()+"\n"
    return text

# print(get_text_from_pdf(pdf_path))