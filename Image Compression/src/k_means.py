import random

import numpy as np


def kmeans(image, n_clusters, max_iterations=100):
    # Load the image and convert to a numpy array
    image_array = np.array(image)

    # Reshape the array to a 2D matrix of pixels
    pixel_matrix = image_array.reshape(-1, 3)

    # Initialize centroids using k-means++
    centroids = initialize_centroids_kmeans_pp(pixel_matrix, n_clusters)

    # Initialize labels
    labels = np.zeros(len(pixel_matrix))

    # Iterate until convergence or maximum iterations
    for i in range(max_iterations):
        # Assign each pixel to its nearest centroid
        distances = np.sqrt(((pixel_matrix - centroids[:, np.newaxis]) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=0)

        # Update the centroids for each channel to the mean of their assigned pixels
        for j in range(n_clusters):
            assigned_pixels = pixel_matrix[labels == j]
            if len(assigned_pixels) > 0:
                centroids[j, 0] = np.mean(assigned_pixels[:, 0])
                centroids[j, 1] = np.mean(assigned_pixels[:, 1])
                centroids[j, 2] = np.mean(assigned_pixels[:, 2])
            else:
                # If a centroid has no assigned pixels, randomly assign a pixel to it
                centroids[j] = np.array(random.sample(list(pixel_matrix), 1))[0]

    # Replace each pixel with its nearest centroid
    compressed_pixels = np.array([centroids[label] for label in labels], dtype=np.uint8)

    # Reshape the compressed pixel matrix to the original shape
    compressed_image_array = compressed_pixels.reshape(image_array.shape)

    return compressed_image_array


def initialize_centroids_kmeans_pp(pixel_matrix, n_clusters):
    # Initialize the first centroid randomly from the pixel values
    centroids = np.zeros((n_clusters, 3))
    centroids[0] = np.array(random.sample(list(pixel_matrix), 1))[0]

    # Initialize the remaining centroids using k-means++
    for i in range(1, n_clusters):
        # Compute the distances to the nearest centroid for each pixel
        distances = np.sqrt(((pixel_matrix - centroids[:i, np.newaxis]) ** 2).sum(axis=2))
        min_distances = np.min(distances, axis=0)

        # Choose the next centroid randomly with probability proportional to the squared distance
        next_centroid = random.choices(pixel_matrix, weights=min_distances ** 2)[0]
        centroids[i] = next_centroid

    return centroids
