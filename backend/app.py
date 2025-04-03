from flask import Flask, request, send_file,  url_for, jsonify
import extract_text
import mask_image
import os
from flask_cors import CORS

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

    return send_file(masked_image_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
