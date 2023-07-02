from step_one import *


def get_histogram(data):
    data_1d = data.flatten()
    count = np.zeros(256)

    for i in range(len(data_1d)):
        count[data_1d[i]] += 1

    return count


if __name__ == "__main__":
    count = get_histogram(get_image_data())
    print(count)
    pixels = np.arange(0, 256, 1)
    print(pixels)
    plt.bar(pixels, count)
    plt.xlabel('color')
    plt.ylabel('count')
    plt.show()
