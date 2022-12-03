import argparse
from typing import Tuple
import cv2
from path import Path

from .dataloader_iam import Batch
from .model import Model
from .preprocessor import Preprocessor

def get_img_height() -> int:
    """Fixed height for NN."""
    return 32

def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
    """Height is fixed for NN, width is set according to training mode (single words or text lines)."""
    if line_mode:
        return 256, get_img_height()
    return 128, get_img_height()

def infer(model: Model, fn_img: Path) -> str:
    """Recognizes text in image provided by file path."""
    img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    batch = Batch([img], None, 1)
    recognized, probability = model.infer_batch(batch, True)
    print(recognized)
    return recognized[0], probability[0]