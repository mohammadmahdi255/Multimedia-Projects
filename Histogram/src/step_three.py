
from step_two import *


def prefix_sum(data):
    counter_values = get_histogram(data)
    counter_keys = np.arange(0, 256, 1)
    for i in range(1, len(counter_values)):
        counter_values[i] = counter_values[i] + counter_values[i - 1]

    return dict(zip(counter_keys, counter_values))


if __name__ == "__main__":
    cumulative_sum = prefix_sum(get_image_data())
    plt.bar(cumulative_sum.keys(), cumulative_sum.values())
    plt.xlabel('color')
    plt.ylabel('count')
    plt.show()
    print(cumulative_sum)
