import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from src.utils.log_business import MyLogger


class ImageHandler:
    def __init__(self, image_path: str, log_path) -> None:
        self.logger = MyLogger('src.image_handler', log_path)
        self.image_path = image_path
        self.image = None

        self.load_image()
        self.convert()

    def load_image(self) -> None:
        self.image = Image.open(self.image_path)

    def convert(self, mode: str = 'YCbCr') -> None:
        self.logger.info('loading image')
        self.image = self.image.convert(mode)

    def to_np_array(self) -> np.ndarray:
        return np.array(self.image.getdata()).reshape(self.image.size + (-1,))

    def show_image(self, image, title):
        self.logger.info('Showing image')
        pil_image = Image.fromarray((np.asarray(image)).astype(np.uint8), mode=self.image.mode)
        plt.figure(figsize=(10, 5))
        plt.imshow(pil_image)
        plt.title(title)
        plt.show()

    def save_image(self, image_layers, filepath):
        self.logger.info('Saving image')
        image_pil = Image.fromarray(image_layers, mode=self.image.mode).convert('RGB')
        image_pil.save(filepath)
