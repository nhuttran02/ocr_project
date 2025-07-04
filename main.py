from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

from ocr_utils import extract_text_paddle
from vietocr_utils import full_ocr_pipeline, detect_residence_yolo, recognize_text_vietocr
from info_extract import extract_info

app = FastAPI()

@app.post("/ocr")
async def ocr_paddle(file: UploadFile = File(...)):
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_paddle(temp_path)
    info = extract_info(text)

    os.remove(temp_path)
    return JSONResponse({"text": text, "info": info})

@app.post("/ocr/vietocr")
async def ocr_vietocr(file: UploadFile = File(...)):
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(temp_path, "rb") as img_f:
        image_bytes = img_f.read()

    text = full_ocr_pipeline(image_bytes)
    info = extract_info(text)

    os.remove(temp_path)
    return JSONResponse({"text": text, "info": info})


@app.post("/ocr/hybrid")
async def ocr_hybrid(file: UploadFile = File(...)):
    temp_path = "temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # YOLO detect residence_content class_id = 4
    residence_crop = detect_residence_yolo(temp_path)
    residence_text = ""
    if residence_crop is not None:
        residence_text = recognize_text_vietocr(residence_crop)

    # PaddleOCR + VietOCR toàn bộ ảnh
    with open(temp_path, "rb") as img_f:
        image_bytes = img_f.read()
    full_text = full_ocr_pipeline(image_bytes)
    info = extract_info(full_text)

    # Ưu tiên residence từ YOLO nếu có
    if residence_text:
        info["residence"] = residence_text

    os.remove(temp_path)
    return JSONResponse({"text": full_text, "info": info})