from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ocr_utils import read_image_bytes, extract_text_paddle

app = FastAPI()

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = read_image_bytes(image_bytes)

        text = extract_text_paddle(image)

        return JSONResponse(content={"text": text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
