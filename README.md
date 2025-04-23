# Document Text Extraction and Masking

This project extracts text from documents (PDFs or images), identifies key data points such as document type, ID, expiry date, person name, DOB, gender, address, country, mobile number, and email using Google Gemini API. The sensitive data is then masked for security and privacy.

Built with **Flask** for the backend and **React** for the frontend, this project aims to automate the process of extracting and sanitizing sensitive information from documents.

---

## Features

- **Text extraction from PDFs and images**: Uses **EasyOCR** for image-based text extraction and **PyMuPDF (fitz)** for PDF-based text extraction.
- **Key data extraction**: Uses **Google Gemini API** to detect specific data from the text (e.g., name, document ID, expiry date).
- **Data masking**: Sensitive data like document ID, expiry date, address, phone number, email, and date of birth are automatically masked for privacy.
- **Techniques used for image preprocessing**:
  - Image rotation
  - Grayscale conversion
  - Monochrome conversion
  - Thresholding (Mean and Gaussian)
  - Deskewing

---

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: React
- **Text Extraction**: EasyOCR, PyMuPDF (fitz)
- **Key Data Extraction**: Google Gemini API
- **Text Masking**: EasyOCR for images, PyMuPDF (fitz) for PDFs

---

## Installation

### Prerequisites

- Python 3.7+
- Node.js and npm (for frontend)
- Google Gemini API key

### Backend Setup (Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/chaitanya06041/Personal-Information-Identification.git
   cd Personal-Information-Identification

2. Install the required Libraries for Backend
   ```bash
   cd Backend
   python -m venv venv
   cd venv/Scripts/activate
   pip install -r requirements.txt
   python app.py

3. Install the required Libraries for Frontend
   - start new terminal
   ```bash
   cd Frontend
   npm install
   npm run dev
