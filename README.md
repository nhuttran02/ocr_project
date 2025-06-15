# OCR Vietnamese ID API (v1.0)

## 🚀 Overview

This project provides a RESTful API for extracting structured information from Vietnamese identity documents (CCCD/CMND/GPLX), using OCR techniques. It currently supports:

- Text recognition using PaddleOCR and/or VietOCR

- Structured info extraction: ID number, full name, DOB, residence, origin, expiry date

- Optional debug output: bounding boxes visualized from OCR result

## 📦 Features

- POST /ocr: OCR with PaddleOCR only

- POST /ocr/vietocr: OCR using VietOCR only

- POST /ocr/hybrid: Combine PaddleOCR + VietOCR

- POST /ocr/structured: Return structured info (ID, name, DOB, etc.)

## 🛠 Installation
```
# Clone the repo
$ git clone https://github.com/nhuttran02/ocr_project.git
$ cd ocr_project

# Create virtual environment
$ python3 -m venv ocr_env
$ source ocr_env/bin/activate

# Install dependencies
$ pip install -r requirements.txt
```
⚠️ Ensure Tesseract or PaddleOCR model weights are available on your system.

## ▶️ Running the server
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
## 📤 Example request

curl -X POST http://localhost:8000/ocr/structured \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_image.jpg"

## ✅ Expected Response
```
{
  "text": "OCR output here",
  "info": {
    "id_number": "xxx",
    "full_name": "yyy",
    "dob": "dd/mm/yyyy",
    "origin": "...",
    "residence": "...",
    "expiry_date": "..."
  }
}
```
## 📂 Project Structure
```
ocr_project/
├── main.py               # FastAPI main entry
├── ocr_utils.py          # OCR related functions
├── vietocr_utils.py      # VietOCR wrapper
├── info_extract.py       # Structured info extractor
├── requirements.txt
└── test_image.jpg        # Sample test image
```
## 📌 Notes

- Performance highly depends on image quality

- Consider combining YOLO for field detection (future plan)


## 👤 Author

Nhut Tran

## 📄 License

MIT License