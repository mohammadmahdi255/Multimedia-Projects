import numpy as np

from utils.log_business import MyLogger


class Quantifying:
    def __init__(self, log_path):
        self.logger = MyLogger('src.quantify', log_path)
        self.QTY = np.array([
            [16, 11, 10, 16, 24, 40, 51, 61],
            [12, 12, 14, 19, 26, 48, 60, 55],
            [14, 13, 16, 24, 40, 57, 69, 56],
            [14, 17, 22, 29, 51, 87, 80, 62],
            [18, 22, 37, 56, 68, 109, 103, 77],
            [24, 35, 55, 64, 81, 104, 113, 92],
            [49, 64, 78, 87, 103, 121, 120, 101],
            [72, 92, 95, 98, 112, 100, 103, 99]
        ])

        self.QTC = np.array([
            [17, 18, 24, 47, 99, 99, 99, 99],
            [18, 21, 26, 66, 99, 99, 99, 99],
            [24, 26, 56, 99, 99, 99, 99, 99],
            [47, 66, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99],
            [99, 99, 99, 99, 99, 99, 99, 99]
        ])

    def quantize(self, dct_coeffs: np.ndarray):
        height, width, depth = dct_coeffs.shape
        quantified = np.zeros((height, width, 3), dtype=np.float32)
        ws = len(self.QTC)
        for k in range(depth):
            channel_data = np.array(dct_coeffs[:, :, k])
            for i in range(0, height, ws):
                for j in range(0, width, ws):
                    if k == 0:
                        quantified[i:i + ws, j:j + ws, k] = np.ceil(channel_data[i:i + ws, j:j + ws] / self.QTY)
                    else:
                        quantified[i:i + ws, j:j + ws, k] = np.ceil(channel_data[i:i + ws, j:j + ws] / self.QTC)
        self.logger.info('finished quantified')
        return quantified

    def de_quantize(self, quantified: np.ndarray):
        height, width, depth = quantified.shape
        dct_coeffs = np.zeros((height, width, 3), dtype=np.float32)
        ws = len(self.QTC)
        for k in range(depth):
            channel_data = np.array(quantified[:, :, k])
            for i in range(0, height, ws):
                for j in range(0, width, ws):
                    if k == 0:
                        dct_coeffs[i:i + ws, j:j + ws, k] = np.round(channel_data[i:i + ws, j:j + ws] * self.QTY)
                    else:
                        dct_coeffs[i:i + ws, j:j + ws, k] = np.round(channel_data[i:i + ws, j:j + ws] * self.QTC)
        self.logger.info('finished de quantified')
        return dct_coeffs
