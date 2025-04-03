import fitz  # PyMuPDF
import re
import json
import os

def mask_sensitive_text(text, sensitive_info):
    """Replace sensitive information in the text with asterisks."""
    for info in sensitive_info:
        if info.strip():
            text = re.sub(re.escape(info), "****", text, flags=re.IGNORECASE)
    return text

def mask_pdf_data(pdf_path, result_json):
    """Mask sensitive information in a PDF and save the modified version."""
    pdf_document = fitz.open(pdf_path)
    masked_pdf_path = os.path.join(os.path.dirname(pdf_path), "masked_" + os.path.basename(pdf_path))

    # Extract sensitive information
    sensitive_info = [
        result_json.get("document_id", ""),
        result_json.get("phone_no", ""),
        result_json.get("address", ""),
        result_json.get("dob", ""),
        result_json.get("expiry_date", "")
    ]
    # Filter out empty values
    sensitive_info = [info for info in sensitive_info if info and info.strip()]
    print("Masking these items:", sensitive_info)

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        
        # Search for each sensitive item individually
        for item in sensitive_info:
            # Find all instances of this sensitive item on the page
            text_instances = page.search_for(item)
            
            # Add redaction annotations for each instance
            for inst in text_instances:
                # Create redaction annotation with black fill
                page.add_redact_annot(inst, fill=(0, 0, 0))
        
        # Apply all redactions on this page
        page.apply_redactions()

    # Save the redacted PDF
    dir_name = os.path.dirname(pdf_path)  # Folder path
    base_name = os.path.basename(pdf_path)  # File name
    masked_pdf_path = os.path.join('masked', f"masked_{base_name}")
    pdf_document.save(masked_pdf_path)
    pdf_document.close()
    print(masked_pdf_path)
    return masked_pdf_path

# Example usage
# pdf_path = "newResume.pdf"
# result_json = {
#     "document_id": "1234-5678-9012",
#     "phone_no": "9876543210",
#     "address": "123 Street Name, City",
#     "dob": "01-01-1990",
#     "expiry_date": "12-12-2030"
# }

# masked_pdf = mask_pdf_text(pdf_path, result_json)
# print(f"Masked PDF saved at: {masked_pdf}")
