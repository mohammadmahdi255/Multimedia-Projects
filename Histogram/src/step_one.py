import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def rgb_to_gray(rgb):
    return np.dot(rgb[..., :3], [0.299, 0.587, 0.114]).astype(int)


def get_image_address(get_input=True):
    if get_input:
        return input('enter address of image: ')
    return input('enter address for saving result: ')


def image_read():
    address = get_image_address()
    image = Image.open(address)
    print('mode of initial image: ' + image.mode)
    return image


def get_image_data():
    image = image_read()
    im_arr = np.array(image)
    gray = rgb_to_gray(im_arr)
    return gray


if __name__ == "__main__":
    gray_img = get_image_data()
    plt.imshow(gray_img, cmap='gray', vmin=0, vmax=255)
    plt.show()
    print(gray_img)
