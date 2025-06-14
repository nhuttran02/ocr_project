from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

from ocr_utils import read_image_bytes, extract_text_paddle
from vietocr_utils import full_ocr_pipeline, recognize_text_vietocr

app = FastAPI()

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    """OCR bằng PaddleOCR toàn ảnh"""
    try:
        image_bytes = await file.read()
        image = read_image_bytes(image_bytes)
        text = extract_text_paddle(image)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/ocr/vietocr")
async def ocr_vietocr(file: UploadFile = File(...)):
    """OCR bằng VietOCR toàn ảnh (không detect box)"""
    try:
        image_bytes = await file.read()
        text = recognize_text_vietocr(image_bytes)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/ocr/hybrid")
async def ocr_hybrid(file: UploadFile = File(...)):
    """OCR kết hợp: PaddleOCR detect box, VietOCR recognize box"""
    try:
        image_bytes = await file.read()
        text = full_ocr_pipeline(image_bytes)
        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
