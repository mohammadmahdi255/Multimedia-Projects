from math import ceil

import numpy as np
import pywt
from PIL import Image


class DiscreteWaveletTransform:
    def __init__(self, block_size, wavelet='haar'):
        if not isinstance(wavelet, str):
            raise TypeError('Wavelet name must be a string')
        try:
            pywt.Wavelet(wavelet).family_name
        except ValueError:
            wavelet = 'haar'
        self.wavelet = wavelet
        self.block_size = block_size

    def perform_dwt(self, image: Image.Image) -> np.ndarray:
        width, height = image.size
        bs = self.block_size
        block_count_x, block_count_y = ceil(width / bs), ceil(height / bs)

        # Pad the image if it cannot be divided exactly into blocks of size `block_size`.
        padded_width = block_count_x * bs
        padded_height = block_count_y * bs
        padded_image = Image.new(mode='RGB', size=(padded_width, padded_height))
        padded_image = padded_image.convert(image.mode)
        padded_image.paste(image, (0, 0))

        dwt_coeffs = np.zeros((padded_height, padded_width, 3), dtype=np.float32)

        for i in range(0, padded_height, bs):
            for j in range(0, padded_width, bs):
                block_image = padded_image.crop((j, i, j + bs, i + bs))
                block_data = np.asarray(block_image.getdata(), dtype=np.float32).reshape((bs, bs, -1))

                for k in range(3):
                    channel_data = np.array(block_data[:, :, k])
                    c_a, (cH, cV, cD) = pywt.dwt2(channel_data, self.wavelet)
                    coeff_block = np.concatenate((
                        np.concatenate((c_a, cH), axis=1),
                        np.concatenate((cV, cD), axis=1)
                    ), axis=0)
                    dwt_coeffs[i:i + bs, j:j + bs, k] = coeff_block

        return dwt_coeffs

    def perform_idwt(self, dwt_coeffs: np.ndarray) -> np.ndarray:
        h, w, d = dwt_coeffs.shape
        bs = self.block_size
        idwt_image = np.zeros((h, w, d), dtype=np.float32)

        for i in range(0, h, bs):
            for j in range(0, w, bs):
                for k in range(d):
                    idwt_block = pywt.idwt2((dwt_coeffs[i:i + bs, j:j + bs, k], (None, None, None)), self.wavelet,
                                            mode='symmetric')
                    idwt_block = idwt_block[:bs, :bs]
                    idwt_image[i:i + bs, j:j + bs, k] = idwt_block

        # Scale the pixel values to the range [0, 255]
        min_val = np.min(idwt_image)
        max_val = np.max(idwt_image)
        idwt_image = (idwt_image - min_val) * (255 / (max_val - min_val))
        idwt_image = np.clip(idwt_image, 0, 255).astype(np.uint8)

        return idwt_image
