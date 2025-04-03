import easyocr
from pdf2image import convert_from_path
from PIL import Image
import os

# Set Poppler path (if needed)
POPPLER_PATH = r"C:\poppler-24.08.0\Library\bin"  # Update with your path

def extract_text_from_pdf(pdf_path):
    """Extract text from an image-based PDF using EasyOCR."""
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)  # Convert PDF pages to images
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader
    extracted_text = ""

    for i, img in enumerate(images):
        img_path = f"temp_page_{i+1}.jpg"
        img.save(img_path, "JPEG")  # Save the image temporarily

        # Use EasyOCR to extract text
        text = reader.readtext(img_path, detail=0)
        extracted_text += f"\n--- Page {i+1} ---\n" + "\n".join(text) + "\n"

        # os.remove(img_path)  # Remove temporary image file

    return extracted_text


# Example usage
pdf_path = 'Aadhar.pdf'
text = extract_text_from_pdf(pdf_path)
print(text)