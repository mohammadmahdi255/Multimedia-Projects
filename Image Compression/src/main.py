from src.huffman import HuffmanTree
from src.image_handler import *
from src.dct import DiscreteCosineTransform
from src.dwt import DiscreteWaveletTransform
from src.quantify import Quantifying
from src.k_means import kmeans


def main_dct(block_size=8):
    huffman_tree = HuffmanTree('log/huffman.log')
    image_handler = ImageHandler("../image/slider_puffin_before_mobile.jpg", 'log/image_handler.log')
    # image_handler.convert('HSV')
    dct = DiscreteCosineTransform(block_size)
    dct_coeffs = dct.perform_dct(image_handler.image)
    image_handler.save_image(dct_coeffs, f'../image/output_dct_{image_handler.image.mode}_{dct.block_size}.jpg')

    dct_coeffs = quantization(huffman_tree, dct_coeffs)

    image_np = dct.perform_idct(dct_coeffs)
    image_handler.show_image(image_np, f'bs={dct.block_size}')
    image_handler.save_image(image_np, f'../image/output_{image_handler.image.mode}_{dct.block_size}.jpg')


def main_dwt(block_size=8):
    huffman_tree = HuffmanTree('log/huffman.log')
    image_handler = ImageHandler("../image/slider_puffin_before_mobile.jpg", 'log/image_handler.log')
    dwt = DiscreteWaveletTransform(block_size)
    dwt_coeffs = dwt.perform_dwt(image_handler.image)
    image_handler.save_image(dwt_coeffs, f'../image/output_dwt_{image_handler.image.mode}_{dwt.block_size}.jpg')

    dwt_coeffs = quantization(huffman_tree, dwt_coeffs)

    image_np = dwt.perform_idwt(dwt_coeffs)
    image_handler.show_image(image_np, f'bs={dwt.block_size}')
    image_handler.save_image(image_np, f'../image/output_watermark_{image_handler.image.mode}_{dwt.block_size}.jpg')


def quantization(huffman_tree, coeffs):
    quantifying = Quantifying('log/quantifying.log')
    quantified = quantifying.quantize(coeffs)

    y_encoded = quantified[:, :, 0]
    cb_encoded = quantified[:, :, 1]
    cr_encoded = quantified[:, :, 2]

    # encoding huffman
    y_root, y_huffman = huffman_tree.encode_array(y_encoded.reshape((-1)))
    cb_root, cb_huffman = huffman_tree.encode_array(cb_encoded.reshape((-1)))
    cr_root, cr_huffman = huffman_tree.encode_array(cr_encoded.reshape((-1)))

    huffman_tree.visualize_tree(y_root).render('output/huffman_tree', format='pdf')

    # to binary string
    y_binary = ''.join([y_huffman[i] for i in y_encoded.reshape((-1))])
    cb_binary = ''.join([cb_huffman[i] for i in cb_encoded.reshape((-1))])
    cr_binary = ''.join([cr_huffman[i] for i in cr_encoded.reshape((-1))])

    # decoding huffman
    y_decoded = huffman_tree.decode(y_root, y_binary).reshape(y_encoded.shape)
    cb_decoded = huffman_tree.decode(cb_root, cb_binary).reshape(cb_encoded.shape)
    cr_decoded = huffman_tree.decode(cr_root, cr_binary).reshape(cr_encoded.shape)
    print(np.array_equal(y_decoded, y_encoded))
    print(np.array_equal(cb_decoded, cb_encoded))
    print(np.array_equal(cr_decoded, cr_encoded))

    quantified[:, :, 0] = y_decoded
    quantified[:, :, 1] = cb_decoded
    quantified[:, :, 2] = cr_decoded

    return quantifying.de_quantize(quantified)


if __name__ == '__main__':
    # for bs in [2, 4, 8, 16, 32, 40, 80]:
    #     print(bs)
    #     main_dct(bs)
    #     main_dwt(bs)
    image_h = ImageHandler("../image/slider_puffin_before_mobile.jpg", 'log/image_handler.log')
    image_h.convert("RGB")
    k = 100
    compressed_image_array = kmeans(image_h.image, k)
    image_h.save_image(compressed_image_array, f'../image/output_{k}_means_{image_h.image.mode}.jpg')



