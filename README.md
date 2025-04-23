# 🔐 PII Detection System

A robust system for identifying **Personally Identifiable Information (PII)** from documents and datasets. This project ensures data privacy and regulatory compliance by automatically detecting and flagging sensitive information like names, emails, phone numbers, and more.

---

## 📌 Features

- ✅ Detects common PII types: Names, Emails, Phone Numbers, SSNs, Credit Card Numbers
- 🔍 Works with plain text, CSV, and PDF files
- 🧠 Combines regex and spaCy NER for accurate detection
- 📊 Outputs categorized results for easy analysis
- 💻 Easy to extend with custom rules or ML models

---

## 🚀 Tech Stack

- **Language**: Python  
- **Libraries**: spaCy, pandas, PyPDF2, re
- **PII Detection**:
  - `regex_detector.py`: Uses regular expressions
  - `spacy_ner_detector.py`: Uses spaCy's NER model

---

## 📁 Project Structure

