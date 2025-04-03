import cv2, os
import easyocr

# result_json = {
#                 'document_type': 'Driving License',
#                 'country': 'INDIA', 
#                 'document_id': 'MHO3 200800000000', 
#                 'email': '', 
#                 'phone_no': '400M4', 
#                 'address': 'KKHANRAMAN NAGAR; BAIGANWADI; Govamdi MUMBAI', 
#                 'dob': '01-12-1987', 
#                 'gender': '', 
#                 'expiry_date': '23-01-2027'
#                }
# image_path = './image.png'

def get_masked_image(image_path, result_json):
    image = cv2.imread(image_path)
    sensitive_info = [
        str(result_json.get("document_id", "")),
        str(result_json.get("phone_no", "")),
        str(result_json.get("address", "")),
        str(result_json.get("dob", "")),
        str(result_json.get("expiry_date", ""))
    ]
    sensitive_info = [str(info) for info in sensitive_info if info is not None]

    chunks = []
    for info in sensitive_info:
        # Add the whole string
        chunks.append(info)
        # Also add individual parts split by spaces
        parts = info.split()
        for part in parts:
            if len(part) >= 3:  # Only consider chunks of reasonable length
                chunks.append(part)

    reader = easyocr.Reader(['en'])
    ocr_results = reader.readtext(image)

    for (bbox, text, prob) in ocr_results:
        # Check if the OCR text matches or is contained in any sensitive info
        detected_text = text.strip()
        
        # Skip very short text (likely to cause false positives)
        if len(detected_text) < 3:
            continue
            
        for chunk in chunks:
            # Case-insensitive comparison
            if (detected_text.lower() in chunk.lower() or 
                chunk.lower() in detected_text.lower()):
                
                # Get bounding box coordinates
                (top_left, top_right, bottom_right, bottom_left) = bbox
                x_min = int(top_left[0])
                y_min = int(top_left[1])
                x_max = int(bottom_right[0])
                y_max = int(bottom_right[1])
                
                # Apply a blur mask over the detected text
                roi = image[y_min:y_max, x_min:x_max]

                # Apply Gaussian Blur to the ROI
                blurred_roi = cv2.GaussianBlur(roi, (15, 15), 30)

                # Replace the original ROI with the blurred ROI
                image[y_min:y_max, x_min:x_max] = blurred_roi
                break
    
    masked_path = os.path.join(os.path.dirname(image_path), "masked_" + os.path.basename(image_path))
    cv2.imwrite(masked_path, image)
    return masked_path
