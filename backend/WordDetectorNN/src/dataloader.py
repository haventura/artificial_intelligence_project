from collections import namedtuple

import cv2
import numpy as np
import torch

DataLoaderItem = namedtuple('DataLoaderItem', 'batch_imgs,batch_gt_maps,batch_aabbs')

class DataLoaderImgFile:
    """loader which simply goes through all jpg files of a directory"""

    def __init__(self, root_dir, input_size, device, max_side_len=1024):
        self.fn_imgs = root_dir.files('*.jpg')
        self.input_size = input_size
        self.device = device
        self.max_side_len = max_side_len

    def ceil32(self, val):
        if val % 32 == 0:
            return val
        val = (val // 32 + 1) * 32
        return val

    def __getitem__(self, item):
        orig = cv2.imread(self.fn_imgs[item], cv2.IMREAD_GRAYSCALE)

        f = min(self.max_side_len / orig.shape[0], self.max_side_len / orig.shape[1])
        if f < 1:
            orig = cv2.resize(orig, dsize=None, fx=f, fy=f)
        img = np.ones((self.ceil32(orig.shape[0]), self.ceil32(orig.shape[1])), np.uint8) * 255
        img[:orig.shape[0], :orig.shape[1]] = orig

        img = (img / 255 - 0.5).astype(np.float32)
        imgs = img[None, None, ...]
        imgs = torch.from_numpy(imgs).to(self.device)
        return DataLoaderItem(imgs, None, None)

    def get_scale_factor(self, item):
        img = cv2.imread(self.fn_imgs[item], cv2.IMREAD_GRAYSCALE)
        f = min(self.max_side_len / img.shape[0], self.max_side_len / img.shape[1])
        return f if f < 1 else 1

    def get_original_img(self, item):
        img = cv2.imread(self.fn_imgs[item], cv2.IMREAD_GRAYSCALE)
        img = (img / 255 - 0.5).astype(np.float32)
        return img

    def __len__(self):
        return len(self.fn_imgs)
