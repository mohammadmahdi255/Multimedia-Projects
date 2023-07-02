from PIL import Image
import numpy as np


def find_closest_palette_color(old_pixel, f=1):
    new_pixel = np.zeros((3,), dtype=np.int32)
    for i in range(3):
        new_pixel[i] = int(round(f * old_pixel[i] / 255) * (255 / f))
    return new_pixel


factor = 8
filename = 'girl'
img = Image.open('image/{}.jpg'.format(filename))
I = np.array(img, dtype=np.int32)

for j in range(I.shape[1]):
    for i in range(I.shape[0]):
        old_pixel = np.copy(I[i][j])
        new_pixel = find_closest_palette_color(old_pixel, factor)
        I[i][j] = new_pixel
        quant_error = old_pixel - new_pixel

        if I[i][j][0] > 255 or I[i][j][1] > 255 or I[i][j][2] > 255 or I[i][j][0] < 0 or I[i][j][1] < 0 or I[i][j][2] < 0:
            print(quant_error)
            print(I[i][j])
            input()

        if i + 1 < I.shape[0]:
            I[i+1][j] = np.int32(I[i+1][j] + quant_error * 7.0 / 16.0)

        if 0 < i and j + 1 < I.shape[1]:
            I[i-1][j+1] = np.int32(I[i-1][j+1] + quant_error * 3.0 / 16.0)

        if j + 1 < I.shape[1]:
            I[i][j+1] = np.int32(I[i][j+1] + quant_error * 5.0 / 16.0)

        if i + 1 < I.shape[0] and j + 1 < I.shape[1]:
            I[i+1][j+1] = np.int32(I[i+1][j+1] + quant_error * 1.0 / 16.0)

img = Image.fromarray(np.uint8(I))
# img.show()
img.save('image/floyd-steinberg-{}-{}.png'.format(factor, filename))
