import numpy as np
import cv2
from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(use_angle_cls=True, lang='vi')

def read_image_bytes(image_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def extract_text_paddle(image: np.ndarray) -> str:
    results = ocr_engine.ocr(image, cls=True)
    extracted_text = ''
    for line in results[0]:
        text = line[1][0]
        extracted_text += text + '\n'
    return extracted_text
