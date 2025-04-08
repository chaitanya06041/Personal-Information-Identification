import cv2
import os
import easyocr
import re
from difflib import SequenceMatcher

def get_masked_image(image_path, result_json):
    image = cv2.imread(image_path)
    
    # Extract sensitive information
    sensitive_info = {
        "document_id": str(result_json.get("document_id", "")),
        "phone_no": str(result_json.get("phone_no", "")),
        "email": str(result_json.get("email", "")),
        "address": str(result_json.get("address", "")),
        "dob": str(result_json.get("dob", "")),
        "expiry_date": str(result_json.get("expiry_date", ""))
    }
    
    # Remove None values and empty strings
    sensitive_info = {k: v for k, v in sensitive_info.items() if v and v.lower() != "none"}
    
    # Initialize EasyOCR
    reader = easyocr.Reader(['en'])
    ocr_results = reader.readtext(image)
    
    # Define patterns for specific data types
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone_no": r'\b(?:\+\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',
        "dob": r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b',
        "expiry_date": r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b',
    }
    
    def text_similarity(text1, text2):
        """Calculate text similarity ratio between two strings"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def normalize_text(text):
        """Normalize text by removing spaces and special characters for comparison"""
        return re.sub(r'[^a-zA-Z0-9]', '', text.lower())
    
    def is_match(ocr_text, sensitive_text, field_type):
        """Determine if OCR text matches sensitive information"""
        # Skip very short text to avoid false positives
        if len(ocr_text) < 3:
            return False
            
        ocr_norm = normalize_text(ocr_text)
        sens_norm = normalize_text(sensitive_text)
        
        # Exact match
        if ocr_norm == sens_norm:
            return True
        
        # For specific field types, use regex pattern matching
        if field_type in patterns:
            if re.search(patterns[field_type], ocr_text):
                # For pattern matches, ensure some level of similarity with expected data
                similarity = text_similarity(ocr_text, sensitive_text)
                return similarity > 0.5
        
        # For document IDs and addresses, use partial matching with higher threshold
        if field_type in ["document_id", "address"]:
            # Check if the OCR text is contained in the sensitive text or vice versa
            if len(ocr_norm) >= 5 and (ocr_norm in sens_norm or sens_norm in ocr_norm):
                return True
            
            # For longer segments, calculate similarity ratio
            if len(ocr_norm) >= 8:
                similarity = text_similarity(ocr_text, sensitive_text)
                return similarity > 0.7
                
        return False
    
    # Process each OCR result
    for (bbox, text, prob) in ocr_results:
        ocr_text = text.strip()
        
        # Skip very short or low confidence detections
        if len(ocr_text) < 3 or prob < 0.5:
            continue
        
        # Check against each type of sensitive information
        for field_type, sensitive_text in sensitive_info.items():
            if sensitive_text and is_match(ocr_text, sensitive_text, field_type):
                # Get bounding box coordinates
                (top_left, top_right, bottom_right, bottom_left) = bbox
                x_min = max(0, int(top_left[0]))
                y_min = max(0, int(top_left[1]))
                x_max = min(image.shape[1], int(bottom_right[0]))
                y_max = min(image.shape[0], int(bottom_right[1]))
                
                # Apply a stronger blur mask for better privacy protection
                roi = image[y_min:y_max, x_min:x_max]
                blurred_roi = cv2.GaussianBlur(roi, (25, 25), 30)
                image[y_min:y_max, x_min:x_max] = blurred_roi
                break
    
    # Ensure the output directory exists
    os.makedirs('masked', exist_ok=True)
    masked_path = os.path.join('masked', "masked_" + os.path.basename(image_path))
    cv2.imwrite(masked_path, image)
    return masked_path