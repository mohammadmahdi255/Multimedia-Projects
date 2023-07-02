
from step_three import *


def mapping(color_levels, cumulative_sum, image_height, image_weight):
    return round((color_levels - 1) * cumulative_sum / (image_height * image_weight))


def section_five():
    data = get_image_data()
    cumulative_sum = prefix_sum(data)
    new_image_array = np.zeros(data.shape)

    for k in cumulative_sum.keys():
        # print(f"{k} {cumulative_sum[k]}")
        cumulative_sum[k] = mapping(
            len(cumulative_sum.keys()), cumulative_sum[k], data.shape[0], data.shape[1])

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            new_image_array[i][j] = cumulative_sum[data[i][j]]

    return new_image_array, cumulative_sum


def save_image(image_pixels, identifier):
    address = get_image_address(get_input=False)
    image = Image.fromarray(image_pixels).convert('LA')
    print(f'{address}/result_{identifier}.png')
    image.save(f'{address}/result_{identifier}.png')


if __name__ == "__main__":
    
    new_image_arr, cumulative_sum_dict = section_five()
    save_image(new_image_arr, identifier='sample')
    plt.imshow(new_image_arr, cmap='gray', vmin=0, vmax=255)
    plt.show()
