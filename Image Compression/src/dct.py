from math import ceil

import cv2
import numpy as np
from PIL import Image


class DiscreteCosineTransform:
    def __init__(self, block_size=8):
        self.block_size = block_size

    def perform_dct(self, image: Image.Image) -> np.ndarray:
        width, height = image.size
        bs = self.block_size
        block_count_x, block_count_y = ceil(width / bs), ceil(height / bs)

        # Pad the image if it cannot be divided exactly into blocks of size `block_size`.
        padded_width = block_count_x * bs
        padded_height = block_count_y * bs
        padded_image = Image.new(mode='RGB', size=(padded_width, padded_height))
        padded_image = padded_image.convert(image.mode)
        padded_image.paste(image, (0, 0))

        dct_coeffs = np.zeros((padded_height, padded_width, 3), dtype=np.float32)

        for i in range(0, padded_height, bs):
            for j in range(0, padded_width, bs):
                block_image = padded_image.crop((j, i, j + bs, i + bs))
                block_data = np.asarray(block_image.getdata(), dtype=np.float32).reshape((bs, bs, -1))

                for k in range(3):
                    channel_data = np.array(block_data[:, :, k])
                    dct_coeffs[i:i + bs, j:j + bs, k] = cv2.dct(channel_data) * (2 * bs)

        return dct_coeffs

    def perform_idct(self, dct_coeffs: np.ndarray) -> np.ndarray:
        h, w, d = dct_coeffs.shape
        bs = self.block_size
        idct_image = np.zeros((h, w, d), dtype=np.float32)

        for i in range(0, h, bs):
            for j in range(0, w, bs):
                for k in range(d):
                    idct_block = cv2.idct(dct_coeffs[i:i + bs, j:j + bs, k] / (2 * bs))
                    idct_image[i:i + bs, j:j + bs, k] = idct_block

        # Scale the pixel values to the range [0, 255]
        min_val = np.min(idct_image)
        max_val = np.max(idct_image)
        idct_image = (idct_image - min_val) * (255 / (max_val - min_val))
        idct_image = np.clip(idct_image, 0, 255).astype(np.uint8)

        return idct_image
