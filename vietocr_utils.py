import io
from PIL import Image
import numpy as np
import cv2

from paddleocr import PaddleOCR
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

# Initialize PaddleOCR for detection
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Initialize VietOCR for recognition
cfg = Cfg.load_config_from_name('vgg_transformer')
# cfg['weights'] = 'vgg_transformer.pth'
cfg['device'] = 'cpu'  # or 'cuda'
vietocr_model = Predictor(cfg)

def recognize_text_vietocr(image_bytes: bytes) -> str:
    """
    Nhận diện text tiếng Việt từ ảnh toàn bộ (không detect)
    """
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return vietocr_model.predict(image)

def read_image_bytes(image_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def crop_image_by_box(image: np.ndarray, box: list) -> Image.Image:
    """
    Cắt vùng chữ theo box PaddleOCR trả về và convert sang PIL để dùng cho VietOCR.
    """
    box = np.array(box).astype(np.int32)
    x, y, w, h = cv2.boundingRect(box)
    cropped = image[y:y+h, x:x+w]
    return Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

def full_ocr_pipeline(image_bytes: bytes) -> str:
    """
    Full pipeline: PaddleOCR detect boxes → crop → VietOCR recognize
    """
    image = read_image_bytes(image_bytes)
    results = paddle_ocr.ocr(image, cls=True)

    final_text = ""

    for line in results[0]:
        box = line[0]
        cropped_img = crop_image_by_box(image, box)
        text = vietocr_model.predict(cropped_img)
        final_text += text + "\n"

    return final_text.strip()
