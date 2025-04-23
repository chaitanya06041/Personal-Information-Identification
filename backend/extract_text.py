from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session
from PIL import Image
import text_from_image
import text_from_pdf
import mask_pdf
import re, json, nltk, itertools, spacy, difflib, math
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from werkzeug.utils import secure_filename
nltk_resources = ["punkt", "maxent_ne_chunker_tab", "words", "averaged_perceptron_tagger", "stopwords"]
import google.generativeai as genai
from dotenv import load_dotenv
import os
import csv
from pathlib import Path
import traceback
from datetime import datetime
import cv2
import easyocr

# for resource in nltk_resources:
#     try:
#         nltk.data.find(f"corpora/{resource}")
#     except LookupError:
#         nltk.download(resource)
GEMINI_API_KEY="AIzaSyAynMJlwBSINKnpaPCIQTW2Q1Qbzl-plVk"
genai.configure(api_key=GEMINI_API_KEY)

# file_path = './image.png'

def get_formatted_text_info(text):
    """Extract structured data using Gemini API"""
    prompt = f"""
    Extract the following details from the text and return JSON:
    - document_type (Resume, Aadhaar, PAN, Driving License, Credit Card, Passport)
    - person name
    - country
    - document_id
    - email
    - phone_no
    - address
    - dob
    - gender
    - expiry_date

    Text: {text}
    Remember that phone number is of 10 or 11 digits only.
    Return JSON with only these keys in lowercase. If not found, use empty string.
    """
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        cleaned_response = re.sub(r'```json|```', '', response.text).strip()
        return json.loads(cleaned_response)
    except Exception as e:
        return {"error": str(e)}
    
def get_data_from_image(image_path):
    image = Image.open(image_path)
    text_content = text_from_image.scan_image_for_text(image)
    print(text_content)
    formated_data = get_formatted_text_info(text_content)
    # print(formated_data)
    return formated_data


def get_data_from_pdf(pdf_path):
    text_content = text_from_pdf.get_text_from_pdf(pdf_path)
    print(text_content)
    formated_data = get_formatted_text_info(text_content)
    print(formated_data)
    return formated_data


def mask_pdf_data(pdf_path):
    formated_data = get_data_from_pdf(pdf_path)
    masked_pdf_path = mask_pdf.mask_pdf_data(pdf_path, formated_data)
    return masked_pdf_path
 
# pdf_path = 'temp.pdf'
# print(mask_pdf_data(pdf_path))
# print('\n')

# img_path = 'uploads/Aadhar Card.jpg'
# print(get_data_from_image(img_path))