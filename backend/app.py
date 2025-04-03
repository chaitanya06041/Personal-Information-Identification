from flask import Flask, request, send_file,  url_for, jsonify
import extract_text
import mask_image
import mask_pdf
import os
from flask_cors import CORS
import base64
from pdf2image import convert_from_bytes

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

@app.route('/mask-pdf', methods=["POST"])
def mask_pdf_endpoint():
    print('request for pdf')
    if 'pdf' not in request.files:
        return {"error" : "No pdf file uploaded"}, 400
    pdf_file = request.files['pdf']
    file_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(file_path)

    json_data = extract_text.get_data_from_pdf(file_path)
    print(json_data)

    masked_pdf_path = mask_pdf.mask_pdf_data(file_path, json_data)
    print('masked pdf: ', masked_pdf_path)
    with open(masked_pdf_path, "rb") as pdf_file:
        base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")


    return jsonify({
        "processed_json" : json_data,
        'masked_pdf_path' : base64_pdf
    })

@app.route('/pdf-to-image', methods=["POST"])
def get_image_from_pdf():
    if 'pdf' not in request.files:
        return {"error" : 'No pdf uploaded'}, 400
    os.makedirs("temp_images", exist_ok=True)
    pdf_file = request.files['pdf'].read()
    images = convert_from_bytes(pdf_file, dpi=300, first_page=1, last_page=1)
    if images:
        image_path = "temp_images/page_1.png"
        os.makedirs("temp_images", exist_ok=True)  # Ensure temp folder exists
        images[0].save(image_path, "PNG")  # Save image

        # Send the image as a response
        return send_file(image_path, mimetype="image/png")

    return {"error": "Failed to process PDF"}, 500
    

if __name__ == '__main__':
    app.run(debug=True)
