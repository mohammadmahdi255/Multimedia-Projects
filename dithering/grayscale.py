from PIL import Image
import numpy as np

filename = 's.jpg'
img = Image.open('image/{}'.format(filename))
pixels = np.array(img)
gray_pixels = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=np.uint8)

for i in range(pixels.shape[0]):
    for j in range(pixels.shape[1]):
        r, g, b = pixels[i][j]
        gray_pixels[i][j] = round(0.299 * r + 0.587 * g + 0.114 * b)

img = Image.fromarray(gray_pixels)
# img.show()
img.save('image/grayscale.png')
