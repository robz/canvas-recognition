import sys
import numpy as np
import matplotlib.pyplot as plt
import math

if len(sys.argv) is not 2:
    print("usage: python read-data.py filename")
    exit()

filename = sys.argv[1]

def plot_images(images, labels):
    n = len(images)
    k = math.ceil(math.sqrt(n))
    plt.figure(figsize=(10, 10))
    for i in range(len(images)):
        plt.subplot(k, k, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(images[i], cmap=plt.cm.binary)
        plt.title(labels[i])
    plt.tight_layout()
    plt.show()

data = np.load(filename + ".npy", allow_pickle=True)
images = data.item().get('images')
labels = data.item().get('labels')

print("loaded", len(images), "training data")

#plot_images(images, labels)
