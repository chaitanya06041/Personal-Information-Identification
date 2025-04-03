from flask import Flask, request, send_file,  url_for, jsonify
import extract_text
import mask_image
import os
from flask_cors import CORS
import base64

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
MASKED_FOLDER = "masked"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MASKED_FOLDER, exist_ok=True)

# masked_image_path = './image2.png'

# print(extract_text.get_data_from_image(file_path))
# json_data = extract_text.get_data_from_image(file_path)
# masked_image_path = mask_image.get_masked_image(file_path, json_data)

@app.route('/mask-image', methods=['POST'])
def mask_image_endpoint():
    print("Received Request")
    if 'image' not in request.files:
        return {"error": "No image file uploaded"}, 400

    image_file = request.files['image']
    
    file_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(file_path)

    json_data = extract_text.get_data_from_image(file_path)
    print(json_data)

    masked_image_path = mask_image.get_masked_image(file_path, json_data) 

    with open(masked_image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode("utf-8")

    return jsonify({
        "processed_json": json_data,
        "masked_image": base64_image
    })

# @app.route('/mask-image', methods=['POST'])
# def mask_image_endpoint():
#     print("Received Request")
#     if 'image' not in request.files:
#         return {"error": "No image file uploaded"}, 400

#     image_file = request.files['image']
    
#     file_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
#     image_file.save(file_path)

#     json_data = {'document_type': 'Aadhaar', 
#                  'person_name': 'Chaitanya Kishor Undale', 
#                  'country': 'India', 
#                  'document_id': '2435 7796 7044', 
#                  'email': '', 
#                  'phone_no': '8767397768', 
#                  'address': '8 KARAD ROAD ATIPO VITA TALUKA KHANAPUR Kheradegita Bhikawadi Kh Sangli Maharashtra 415311', 
#                  'dob': '06/10/2004', 
#                  'gender': 'MALE', 
#                  'expiry_date': ''
#                  }
#     print(json_data)

#     masked_image_path = file_path 

#     with open(masked_image_path, "rb") as img_file:
#         base64_image = base64.b64encode(img_file.read()).decode("utf-8")

#     return jsonify({
#         "processed_json": json_data,
#         "masked_image": base64_image
#     })

if __name__ == '__main__':
    app.run(debug=True)
