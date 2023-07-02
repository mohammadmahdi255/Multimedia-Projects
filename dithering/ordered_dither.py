from PIL import Image
import numpy as np


def dither_matrix(n: int):
    if n == 1:
        return np.array([[0]])
    else:
        first = (n ** 2) * dither_matrix(int(n/2))
        second = (n ** 2) * dither_matrix(int(n/2)) + 2
        third = (n ** 2) * dither_matrix(int(n/2)) + 3
        fourth = (n ** 2) * dither_matrix(int(n/2)) + 1
        first_col = np.concatenate((first, third), axis=0)
        second_col = np.concatenate((second, fourth), axis=0)
        return (1/n**2) * np.concatenate((first_col, second_col), axis=1)


filename = 'grayscale.png'
img = Image.open('image/{}'.format(filename))
I = np.array(img)
O = np.zeros((I.shape[0], I.shape[1]), dtype=np.uint8)

n = 16
D = dither_matrix(n)

for i in range(I.shape[0]):
    for j in range(I.shape[1]):
        l = i % n
        k = j % n

        if float(I[i][j])/255 > D[l][k]:
            O[i][j] = 255
        else:
            O[i][j] = 0

print(O)
img = Image.fromarray(O)
img.show()
img.save('image/ordered-dither-{}-{}'.format(n, filename))
