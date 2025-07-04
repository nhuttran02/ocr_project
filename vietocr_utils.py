import numpy as np
import cv2
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR
from ultralytics import YOLO

# PaddleOCR
paddle_ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# VietOCR
config = Cfg.load_config_from_name('vgg_transformer')
# config['weights'] = 'model/vietocr_model.pth'
config['device'] = 'cpu'
vietocr_model = Predictor(config)

yolo_model = YOLO("model/yolo_detect.pt")

yolo_classes = ['full_name_content', 'gender_content', 'id_number_content', 'origin_content', 'residence_content']


def read_image_bytes(image_bytes: bytes) -> np.ndarray:
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def crop_image_by_box(image: np.ndarray, box: list) -> Image.Image:
    box = np.array(box).astype(np.int32)
    x, y, w, h = cv2.boundingRect(box)
    cropped = image[y:y+h, x:x+w]
    return Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

def full_ocr_pipeline(image_bytes: bytes) -> str:
    image = read_image_bytes(image_bytes)
    results = paddle_ocr.ocr(image, cls=True)

    final_text = ""
    for line in results[0]:
        box = line[0]
        cropped_img = crop_image_by_box(image, box)
        text = vietocr_model.predict(cropped_img)
        final_text += text + "\n"

    return final_text.strip()


def recognize_text_vietocr(image: np.ndarray) -> str:
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return vietocr_model.predict(pil_img)


def detect_residence_yolo(image_path: str):
    results = yolo_model.predict(source=image_path, conf=0.25)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            class_id = int(box.cls)
            if yolo_classes[class_id] == 'residence_content':
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                img = cv2.imread(image_path)
                residence_crop = img[y1:y2, x1:x2]
                return residence_crop

    return None